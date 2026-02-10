import Papa from 'papaparse';

/**
 * Parses the User's Tax-Lot CSV and prepares it for the HIFO engine.
 */
export const parseTaxLots = (file) => {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      header: true,            // Use the first row as keys (Asset, Date, etc.)
      skipEmptyLines: true,
      dynamicTyping: true,     // Automatically converts numbers and booleans
      complete: (results) => {
        // Post-processing: Calculate Total Cost per lot
        const cleanedData = results.data.map(lot => ({
          ...lot,
          total_cost: (lot.Quantity * lot.Cost_Basis_Per_Unit) + (lot.Fee_Paid || 0),
          is_long_term: checkIsLongTerm(lot.Date_Acquired)
        }));
        resolve(cleanedData);
      },
      error: (error) => reject(error)
    });
  });
};

// Helper to determine if a lot qualifies for lower Long-Term Capital Gains tax
const checkIsLongTerm = (dateString) => {
  const acquisitionDate = new Date(dateString);
  const oneYearAgo = new Date();
  oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
  return acquisitionDate <= oneYearAgo;
};
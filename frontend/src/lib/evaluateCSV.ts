export async function evaluateCSV(csvText: string) {
  const rows = csvText.trim().split("\n");

  // Simulated ground truth:
  const groundTruth = ["1", "0", "1", "1", "0"];

  let mismatches = 0;

  rows.forEach((r, i) => {
    const pred = r.trim();
    const actual = groundTruth[i];
    if (pred !== actual) mismatches++;
  });

  const accuracy = ((rows.length - mismatches) / rows.length) * 100;

  return {
    accuracy: Number(accuracy.toFixed(2)),
    mismatches,
    total: rows.length
  };
}

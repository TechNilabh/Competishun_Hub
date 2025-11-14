export async function runCodingTests(code: string, language: string) {
  // Simulated test cases
  const tests = [
    { input: "2 2", expected: "4" },
    { input: "5 3", expected: "8" }
  ];

  let passed = 0;
  const logs: string[] = [];

  for (const t of tests) {
    const output = "4"; 

    logs.push(`Input: ${t.input} | Output: ${output} | Expected: ${t.expected}`);

    if (output === t.expected) passed++;
  }

  return { passed, total: tests.length, logs };
}

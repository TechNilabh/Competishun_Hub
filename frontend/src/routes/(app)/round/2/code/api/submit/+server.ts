import type { RequestHandler } from "@sveltejs/kit";
import { writeFileSync, mkdirSync } from "fs";
import testcases from "$lib/data/testcases/round2.json";
import { exec } from "child_process";
import os from "os";
import path from "path";

export const POST: RequestHandler = async ({ request }) => {
    const { code, language } = await request.json();

    const tempRoot = os.tmpdir();
    const dir = path.join(tempRoot, `submit-${Date.now()}`);
    mkdirSync(dir, { recursive: true });

    const filenameMap = {
        python: "solution.py",
        c: "solution.c",
        cpp: "solution.cpp"
    };

    const filename = filenameMap[language];
    const filepath = `${dir}/${filename}`;

    writeFileSync(filepath, code);

    let runCmd = "";
    if (language === "python") {
        runCmd = `python "${filepath}"`;
    } else if (language === "c") {
        runCmd = `gcc "${filepath}" -o "${dir}/a.out" && "${dir}/a.out"`;
    } else if (language === "cpp") {
        runCmd = `g++ "${filepath}" -o "${dir}/a.out" && "${dir}/a.out"`;
    }

    let results = "";

    for (const t of testcases) {
        const inputPath = `${dir}/input.txt`;
        writeFileSync(inputPath, t.input);

        const execCmd = `${runCmd} < "${inputPath}"`;

        const output: string = await new Promise((resolve) => {
            exec(execCmd, { timeout: 5000 }, (err, stdout, stderr) => {
                resolve((stderr || stdout).trim());
            });
        });

        const ok = output === t.expected ? "PASSED" : "FAILED";

        results += `
Test Case:
Input: ${t.input}
Output: ${output}
Expected: ${t.expected}
Result: ${ok}
`;
    }

    return new Response(JSON.stringify({ output: results }));
};

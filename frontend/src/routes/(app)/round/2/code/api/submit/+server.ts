import type { RequestHandler } from "@sveltejs/kit";
import { writeFileSync, mkdirSync } from "fs";
import testcases from "$lib/data/testcases/round2.json";
import { exec } from "child_process";
import os from "os";
import path from "path";

export const POST: RequestHandler = async ({ request }) => {
    const { code, language } = await request.json();

    // temp folder
    const dir = path.join(os.tmpdir(), `submit-${Date.now()}`);
    mkdirSync(dir, { recursive: true });

    const filenameMap = {
        python: "solution.py",
        c: "solution.c",
        cpp: "solution.cpp"
    } as const;

    const filename = filenameMap[language];
    const filepath = `${dir}/${filename}`;

    writeFileSync(filepath, code);

    // Compile + run commands
    let runCmd = "";
    if (language === "python") {
        runCmd = `python "${filepath}"`;
    } else if (language === "c") {
        runCmd = `gcc "${filepath}" -o "${dir}/a.out" && "${dir}/a.out"`;
    } else if (language === "cpp") {
        runCmd = `g++ "${filepath}" -o "${dir}/a.out" && "${dir}/a.out"`;
    }

    const results: Array<{
        input: string;
        expected: string;
        output: string;
        passed: boolean;
    }> = [];

    for (const t of testcases) {
        const inputPath = `${dir}/input.txt`;
        writeFileSync(inputPath, t.input);

        const execCmd = `${runCmd} < "${inputPath}"`;

        const output: string = await new Promise((resolve) => {
            exec(execCmd, { timeout: 5000 }, (err, stdout, stderr) => {
                resolve((stderr || stdout).trim());
            });
        });

        results.push({
            input: t.input,
            expected: t.expected,
            output,
            passed: output === t.expected
        });
    }

    return new Response(
        JSON.stringify({
            total: testcases.length,
            preview: testcases.slice(0, 5),
            results
        })
    );
};

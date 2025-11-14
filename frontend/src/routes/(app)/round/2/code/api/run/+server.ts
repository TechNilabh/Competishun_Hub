import type { RequestHandler } from "@sveltejs/kit";
import { writeFileSync, mkdirSync } from "fs";
import { exec } from "child_process";
import path from "path";
import crypto from "crypto";

export const POST: RequestHandler = async ({ request }) => {
    const tempRoot = path.join(process.cwd(), "sandbox-temp");
    const dir = path.join(tempRoot, "code-" + crypto.randomUUID());
    mkdirSync(dir, { recursive: true });

    const filenameMap = {
        python: "solution.py",
        c: "solution.c",
        cpp: "solution.cpp"
    } as const;

    type Language = keyof typeof filenameMap;

    const { code, language, input } = await request.json() as {
        code: string; language: Language; input: string;
    };

    const filename = filenameMap[language];
    const filepath = path.join(dir, filename);
    writeFileSync(filepath, code);

    // Write input safely to a file so Python/C/C++ receive EXACT stdin
    const inputFile = path.join(dir, "input.txt");
    writeFileSync(inputFile, input);

    // Determine run command
    let runCmd = "";
    switch (language) {
        case "python":
            runCmd = `python "${filepath}"`;
            break;
        case "c":
            runCmd = `gcc "${filepath}" -o "${dir}/a.out" && "${dir}/a.out"`;
            break;
        case "cpp":
            runCmd = `g++ "${filepath}" -o "${dir}/a.out" && "${dir}/a.out"`;
            break;
    }

    // Attach stdin redirection
    const finalCmd = `${runCmd} < "${inputFile}"`;

    return new Promise((resolve) => {
        exec(finalCmd, { timeout: 8000 }, (err, stdout, stderr) => {
            resolve(new Response(JSON.stringify({
                output: (stderr || stdout || "").trim()
            })));
        });
    });
};

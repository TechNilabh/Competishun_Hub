import { exec } from "child_process";
import type { RequestHandler } from "@sveltejs/kit";
import { writeFileSync } from "fs";

export const POST: RequestHandler = async ({ request }) => {
    const { code } = await request.json();

    const file = "/tmp/submission.py";
    writeFileSync(file, code);

    const testCases = [
        { input: "2", expected: "4" },
        { input: "10", expected: "20" }
    ];

    let results = "";

    for (let t of testCases) {
        try {
            const result = await new Promise<string>((resolve) => {
                exec(`echo "${t.input}" | python3 ${file}`, (err, stdout) => {
                    resolve(stdout.trim());
                });
            });

            const status = result === t.expected ? "PASSED" : "FAILED";
            results += `Input: ${t.input}\nOutput: ${result}\nExpected: ${t.expected}\n=> ${status}\n\n`;

        } catch (error) {
            results += "Runtime Error\n";
        }
    }

    return new Response(JSON.stringify({ output: results }));
};

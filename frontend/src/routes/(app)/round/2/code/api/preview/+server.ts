import testcases from "$lib/data/testcases/round2.json";

export function GET() {
    return new Response(
        JSON.stringify(testcases.slice(0, 5))
    );
}

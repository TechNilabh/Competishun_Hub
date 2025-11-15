import type { RequestHandler } from '@sveltejs/kit';

const DJANGO_URL = 'http://127.0.0.1:8000/api/ml/leaderboard/';

export const GET: RequestHandler = async () => {
    const res = await fetch(DJANGO_URL);

    const contentType = res.headers.get("content-type");
    if (!contentType?.includes("application/json")) {
        const text = await res.text();
        console.error("Backend error:", text);
        return new Response(JSON.stringify({ error: "Backend returned non-JSON" }), { status: 500 });
    }

    const data = await res.json();
    return new Response(JSON.stringify(data), { status: 200 });
};

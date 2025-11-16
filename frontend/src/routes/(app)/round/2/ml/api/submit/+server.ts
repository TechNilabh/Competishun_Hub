import type { RequestHandler } from '@sveltejs/kit';

const DJANGO_SUBMIT_URL = 'http://127.0.0.1:8000/api/ml/submit/';

export const POST: RequestHandler = async ({ request }) => {
    try {
        const formData = await request.formData();
        const file = formData.get("file");

        if (!file || !(file instanceof File)) {
            return new Response(JSON.stringify({ error: "file missing" }), { status: 400 });
        }

        // Forward to Django
        const djangoForm = new FormData();
        djangoForm.append("file", file, file.name);

        const res = await fetch(DJANGO_SUBMIT_URL, {
            method: "POST",
            credentials: "include",
            body: djangoForm
        });

        const data = await res.json();

        return new Response(JSON.stringify(data), {
            status: res.status,
            headers: { "Content-Type": "application/json" }
        });

    } catch (err) {
        console.error("Submit Error:", err);
        return new Response(JSON.stringify({ error: "Internal server error" }), { status: 500 });
    }
};

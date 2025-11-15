import { redirect } from "@sveltejs/kit";

export function load({ cookies, url }) {
    const step = Number(cookies.get("codeFlowStep") || "0");
    const path = url.pathname;

    if (path.includes("/fullscreen") && step > 1) {
        throw redirect(303, "/round/2/code/start");
    }

    if (path.includes("/editor") && step > 2) {
        throw redirect(303, "/round/2/code/start");
    }

    if (path.includes("/completed") && step > 3) {
        throw redirect(303, "/round/2/code/start");
    }

    return { step };
}

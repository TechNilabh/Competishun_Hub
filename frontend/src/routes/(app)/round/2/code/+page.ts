import { redirect } from "@sveltejs/kit";

export function load() {
    throw redirect(302, "/round/2/code/start");
}

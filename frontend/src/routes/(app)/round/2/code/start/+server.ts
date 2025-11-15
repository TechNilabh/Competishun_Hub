import { redirect } from "@sveltejs/kit";

export const POST = async ({ cookies }: any) => {
    cookies.set("codeFlowStep", "1", {
        path: "/",
        httpOnly: true,
        sameSite: "strict",
        secure: false
    });

    throw redirect(303, "/round/2/code/fullscreen");
};

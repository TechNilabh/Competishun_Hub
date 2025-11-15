import { writable } from "svelte/store";
import { browser } from "$app/environment";

export const codeFlow = writable({
    step: 1,
    fullScreenExited: false,
    code: "",
    timer: 30 * 60
});

if (browser) {
    const saved = localStorage.getItem("codeFlow");
    if (saved) codeFlow.set(JSON.parse(saved));

    codeFlow.subscribe((v) => {
        localStorage.setItem("codeFlow", JSON.stringify(v));
    });
}

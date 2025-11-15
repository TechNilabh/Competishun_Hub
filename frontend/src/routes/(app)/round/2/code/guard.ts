export function protect(requiredStep: number) {
    const saved = localStorage.getItem("codeFlow");
    if (!saved) return false;
    const data = JSON.parse(saved);
    return data.step >= requiredStep;
}

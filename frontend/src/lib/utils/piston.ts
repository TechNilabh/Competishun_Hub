const PISTON_API = 'https://emkc.org/api/v2/piston';

export interface ExecutionResult {
  stdout: string;
  stderr: string;
  output: string;
  code: number;
  signal: string | null;
}

export async function executeCode(
  language: string,
  code: string,
  stdin: string = ''
): Promise<ExecutionResult> {
  const languageMap: Record<string, { name: string; version: string }> = {
    python: { name: 'python', version: '3.10.0' },
    c: { name: 'c', version: '10.2.0' },
    cpp: { name: 'c++', version: '10.2.0' },
    java: { name: 'java', version: '15.0.2' },
    javascript: { name: 'javascript', version: '18.15.0' },
  };

  const langConfig = languageMap[language];
  if (!langConfig) {
    throw new Error(`Unsupported language: ${language}`);
  }

  const response = await fetch(`${PISTON_API}/execute`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      language: langConfig.name,
      version: langConfig.version,
      files: [
        {
          name: `main.${getFileExtension(language)}`,
          content: code,
        },
      ],
      stdin,
      args: [],
      compile_timeout: 10000,
      run_timeout: 5000,
    }),
  });

  if (!response.ok) {
    throw new Error('Code execution failed');
  }

  const result = await response.json();
  return result.run || result;
}

function getFileExtension(language: string): string {
  const extensions: Record<string, string> = {
    python: 'py',
    c: 'c',
    cpp: 'cpp',
    java: 'java',
    javascript: 'js',
  };
  return extensions[language] || 'txt';
}

export async function getAvailableRuntimes() {
  const response = await fetch(`${PISTON_API}/runtimes`);
  if (!response.ok) {
    throw new Error('Failed to fetch runtimes');
  }
  return response.json();
}
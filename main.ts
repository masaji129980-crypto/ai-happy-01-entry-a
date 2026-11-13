// "Warm Sunrise" — ai-happy-01 entry (Node 22, standard library only).
// Copies the entry.png beside this file to the output directory.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, 'entry.png');
if (!existsSync(src)) {
  throw new Error(`entry.png not found beside main.ts (${src})`);
}
const size = statSync(src).size;
if (size > 1024 * 1024) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB limit`);
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(src, join(outDir, 'entry.png'));
console.log(`Warm Sunrise: copied entry.png (${size} bytes) to ${join(outDir, 'entry.png')}`);

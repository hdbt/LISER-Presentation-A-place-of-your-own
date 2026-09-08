"""Rebuild from bundled snapshots. Run from any working directory."""
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run(args):
    print('+', ' '.join(map(str, args)), flush=True)
    subprocess.run(list(map(str, args)), cwd=ROOT, check=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quarto', default=os.environ.get('QUARTO_BIN', 'quarto'))
    parser.add_argument('--node', default=os.environ.get('NODE_BIN', 'node'))
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    run([sys.executable, 'scripts/verify_inputs.py'])
    run([sys.executable, 'scripts/build_geometry.py'])
    run([sys.executable, 'scripts/build_data.py'])
    run([sys.executable, 'scripts/verify_results.py'])
    for source in ['LISER_Combined.qmd']:
        run([args.quarto, 'render', source])
    run([args.node, 'scripts/check_controls.cjs', 'LISER_Combined.html'])
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for name in ['LISER_Combined.html']:
            shutil.copy2(ROOT / name, args.output_dir / name)
    report = {'python':sys.version, 'quarto':subprocess.check_output([args.quarto,'--version'],text=True).strip(),
              'node':subprocess.check_output([args.node,'--version'],text=True).strip(), 'status':'passed',
              'checks':'input hashes, geometry and data snapshot equality, baseline calculations, 12 slide DOM control states',
              'visual_review':'not performed by build; inspect at presentation resolution'}
    (ROOT/'BUILD_REPORT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('PASS: presentation rebuilt.')

if __name__ == '__main__': main()

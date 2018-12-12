{ pkgs ? import <nixpkgs> {} }: with pkgs; let
  python-with-packages = python3.withPackages (pypkgs: with pypkgs; [
    numpy
    pygame
  ]);
in runCommand "graph-tycoon" {
  buildInputs = [ python-with-packages makeWrapper ];
} ''
  mkdir -p $out/bin $out/src
  (cd ${./src}
     find . -name '*.py' -exec cp --no-preserve=mode --parents -t $out/src {} \;
  )
  makeWrapper ${python-with-packages}/bin/python $out/bin/graph-tycoon \
    --add-flags $out/src/main.py
''

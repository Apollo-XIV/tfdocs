{
  pkgs,
  deps
}:
pkgs.stdenv.mkDerivation {
  name = "tfdocs";
  src = ./.;
  buildInputs = deps;
  buildPhase = ''
    run pyinstaller-build
  '';
  installPhase = ''
    mkdir -p $out/bin
    mv dist/tfdocs $out/bin/
  '';
  meta = with pkgs.lib; {
    description = "Terraform provider documentation viewer for the command-line";
    license = licenses.mit;
    maintainers = ["alex@crease.sh"];
  };
}

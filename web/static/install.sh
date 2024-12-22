# download tfdocs.AppImage
curl -O https://tfdocs.crease.sh/releases/latest/download

# make sure the bin is executable
chmod +x tfdocs.AppImage

OUTDIR=/usr/local/bin
# check that the output directory is on the path
if [[ ":$PATH:" == *":$OUTDIR:"* ]]; then
  echo "Directory '$OUTDIR' is in PATH. Installing to $OUTDIR."
  # move the bin to a location on the user's path
  mv tfdocs.AppImage "$OUTDIR/tfdocs"
else
  echo "Directory '$OUTDIR' is NOT in PATH, exiting."
  exit 1
fi


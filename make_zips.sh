#!/bin/bash
# Rebuild the download bundles from the source-of-truth folders
cd "$(dirname "$0")/deliverables"
rm -f Spruce_Lights_Content_Pack_Oct2026.zip Spruce_Pro_Content_Pack_Oct2026.zip Spruce_Videos_Pack_Oct2026.zip
zip -qr Spruce_Lights_Content_Pack_Oct2026.zip spruce_lights
zip -qr Spruce_Pro_Content_Pack_Oct2026.zip spruce_pro
cd .. && zip -qr deliverables/Spruce_Videos_Pack_Oct2026.zip videos -x '*.DS_Store' 'videos/spruce_lights_real/*'
zip -qr deliverables/Spruce_RealLights_Videos_Oct2026.zip videos/spruce_lights_real
echo "zips rebuilt in deliverables/"

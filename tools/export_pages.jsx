// Run in InDesign (File > Scripts, or via osascript) with the brochure open.
// Exports Version C pages (document pages 41-60) as JPEGs for tools/make_spreads.py.
var OUT = "/Users/subhranilmaity/Downloads/SUNDREX BROCHURE/Showcase - Sketchbook/tools/pages/";
Folder(OUT).create();
var d = app.activeDocument, p = app.jpegExportPreferences;
p.jpegExportRange = ExportRangeOrAllPages.EXPORT_RANGE;
p.exportingSpread = false; p.exportResolution = 160; p.jpegQuality = JPEGOptionsQuality.MAXIMUM;
p.antiAlias = true; p.useDocumentBleeds = false; p.jpegColorSpace = JpegColorSpaceEnum.RGB;
for (var n = 1; n <= 20; n++){
  p.pageString = "+" + (40 + n);
  d.exportFile(ExportFormat.JPG, File(OUT + "p" + (n < 10 ? "0" : "") + n + ".jpg"), false);
}
"exported 20 pages to " + OUT;

"""Checks for portable image embedding and the raw-material boundary."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import patch
import base64

import build_graph


class FigureEmbeddingTests(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.note = self.root / "topics" / "test.md"
        self.note.parent.mkdir()
        self.figures = self.root / "assets" / "figures"
        self.figures.mkdir(parents=True)
        patcher = patch.object(build_graph, "ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_finished_svg_is_embedded(self):
        payload = b'<svg xmlns="http://www.w3.org/2000/svg"></svg>'
        (self.figures / "plot.svg").write_bytes(payload)
        result = build_graph.embed_note_figures(
            "![Accessible caption](../assets/figures/plot.svg)", self.note)
        self.assertEqual(result, "![Accessible caption](data:image/svg+xml;base64,"
                         + base64.b64encode(payload).decode() + ")")

    def test_raw_sources_cannot_be_embedded(self):
        raw = self.root / "sources"
        raw.mkdir()
        (raw / "private.png").write_bytes(b"private material")
        with self.assertRaisesRegex(ValueError, "assets/figures"):
            build_graph.embed_note_figures("![Raw](../sources/private.png)", self.note)

    def test_missing_figure_fails_clearly(self):
        with self.assertRaisesRegex(ValueError, "missing figure"):
            build_graph.embed_note_figures("![Missing](../assets/figures/missing.svg)", self.note)

    def test_traversal_outside_finished_figures_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "assets/figures"):
            build_graph.embed_note_figures(
                "![Raw](../assets/figures/../../sources/private.png)", self.note)

    def test_remote_images_are_not_downloaded(self):
        markdown = "![Remote](https://example.com/plot.png)"
        self.assertEqual(build_graph.embed_note_figures(markdown, self.note), markdown)


if __name__ == "__main__":
    main()

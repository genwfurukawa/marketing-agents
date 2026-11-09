"""Synthetic provider metadata: citation extraction makes no model calls."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from extractors import extract_brightdata_sources, extract_openai, extract_claude, extract_gemini, extract_perplexity
from brightdata import extract_row


class SourceExtractionTests(unittest.TestCase):
    def test_brightdata_classic_and_grouped_chatgpt_chips(self):
        row = {'answer_html': '<span data-testid="webpage-citation-pill"><a href="https://first.example/a?x=1&amp;y=2">Source</a></span><a href="https://not-cited.example">Other link</a>'}
        cited, retrieved = extract_brightdata_sources(row)
        self.assertEqual(cited, ['https://first.example/a?x=1&y=2'])
        payload = json.dumps([{'url': 'https://first.example'}, {'url': 'https://second.example'}]).replace('"', '&quot;')
        cited, _ = extract_brightdata_sources({'answer_html': f'<span data-assistant-sources-payload="{payload}"></span>'})
        self.assertEqual(cited, ['https://first.example', 'https://second.example'])

    def test_perplexity_sources_bound_by_chips_or_provider_flag(self):
        row = {'sources': [{'url': 'https://cited.example', 'domain': 'Wrong display label'},
                           {'url': 'https://retrieved.example'}, {'url': 'https://flagged.example', 'cited': True}],
               'answer_html': '<span data-pplx-citation data-pplx-citation-url="https://cited.example">1</span>'}
        cited, retrieved = extract_brightdata_sources(row)
        self.assertEqual(set(cited), {'https://cited.example', 'https://flagged.example'})
        self.assertEqual(retrieved[0]['domain'], 'retrieved.example')

    def test_unbound_results_markdown_images_and_invalid_urls_never_become_citations(self):
        row = {'search_sources': [{'url': 'https://retrieved.example', 'domain': 'Arbitrary label'}],
               'citations': [{'url': 'javascript:alert(1)'}, {'url': 'https://unused.example', 'cited': False}],
               'answer_html': '<span data-assistant-sources-payload="broken"></span><a href="https://unrelated.example">link</a>'}
        cited, retrieved = extract_brightdata_sources({**row, 'answer_text_markdown':'[More](https://linked.example) ![Image](https://images.example/a.png)'})
        self.assertEqual(cited, [])
        self.assertEqual({s['url'] for s in retrieved}, {'https://retrieved.example', 'https://unused.example'})

    def test_explicit_citations_are_deduplicated_and_chip_can_confirm_false_flag(self):
        url = 'https://example.com/source'
        cited, retrieved = extract_brightdata_sources({'citations': [{'url': url}, {'url': url}],
            'sources': [{'url': url, 'cited': False}], 'answer_html': f'<span data-pplx-citation-url="{url}"></span>'})
        self.assertEqual(cited, [url]); self.assertEqual(retrieved, [])

    def test_unusable_optional_html_does_not_fail_valid_capture(self):
        text, cited, _ = extract_row({'answer_text': 'A complete provider answer.',
            'citations': [{'url': 'https://structured.example'}],
            'answer_html': '<![unsupported[content]]>'})
        self.assertEqual(text, 'A complete provider answer.')
        self.assertEqual(cited, ['https://structured.example'])

    def test_openai_annotations_are_not_retrieved_results(self):
        raw = {'output': [{'type': 'web_search_call', 'action': {'sources': [{'url': 'https://unused.example'}]}},
                          {'type': 'message', 'content': [{'type': 'output_text', 'text': 'Answer', 'annotations': [{'type': 'url_citation', 'url': 'https://cited.example'}]}]}]}
        _, cited, sources, searched = extract_openai(raw)
        self.assertEqual(cited, ['https://cited.example']); self.assertEqual(len(sources), 1); self.assertTrue(searched)

    def test_claude_citation_blocks_are_not_search_results(self):
        raw = {'content': [{'type': 'text', 'text': 'Answer', 'citations': [{'url': 'https://cited.example'}]},
                           {'type': 'web_search_tool_result', 'content': [{'url': 'https://unused.example'}]}]}
        _, cited, sources, _, _ = extract_claude(raw)
        self.assertEqual(cited, ['https://cited.example']); self.assertEqual(len(sources), 1)

    def test_gemini_grounding_supports_select_only_used_chunks(self):
        raw = {'candidates': [{'content': {'parts': [{'text': 'Answer'}]}, 'groundingMetadata': {
            'groundingChunks': [{'web': {'uri': 'https://unused.example'}}, {'web': {'uri': 'https://cited.example'}}],
            'groundingSupports': [{'groundingChunkIndices': [1]}]}}]}
        _, cited, sources, _ = extract_gemini(raw)
        self.assertEqual(cited, ['https://cited.example']); self.assertEqual(len(sources), 2)

    def test_gemini_invalid_grounding_indices_cannot_bind_another_source(self):
        raw = {'candidates': [{'content': {'parts': [{'text': 'Answer'}]}, 'groundingMetadata': {
            'groundingChunks': [{'web': {'uri': 'https://unused.example'}}],
            'groundingSupports': [{'groundingChunkIndices': [-1, 99, '0', True]}]}}]}
        self.assertEqual(extract_gemini(raw)[1], [])

    def test_perplexity_api_requires_reference_or_annotation(self):
        raw = {'output_text': 'Evidence [web:used]', 'output': [{'type': 'search_results', 'results': [
            {'id': 'used', 'url': 'https://cited.example'}, {'id': 'unused', 'url': 'https://unused.example'}]}]}
        _, cited, sources = extract_perplexity(raw)
        self.assertEqual(cited, ['https://cited.example']); self.assertEqual(len(sources), 2)


if __name__ == '__main__':
    unittest.main()

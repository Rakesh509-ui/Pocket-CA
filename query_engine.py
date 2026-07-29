from __future__ import annotations

from typing import Sequence

from llama_index.core.schema import QueryBundle

from PocketCA.citation_builder import prepare_citation_context, format_citations
from PocketCA.models import QueryResult
from PocketCA.retriever import get_hybrid_retriever
from PocketCA.settings import configure_settings


def _join_citable_texts(nodes: Sequence) -> str:
	parts: list[str] = []
	for node in nodes:
		text = getattr(node.node, "text", None) or ""
		if text:
			parts.append(text.strip())
	return "\n\n".join(parts)


def answer_question(question: str) -> QueryResult:
	"""Answer a tax-law question using the graph retriever.

	This implementation performs retrieval, prepares citation-context nodes
	and returns a simple concatenation of citable node excerpts together
	with a formatted source list. It intentionally keeps the LLM step
	out to avoid hard runtime dependencies in the development environment.
	"""
	configure_settings()

	retriever = get_hybrid_retriever()
	if not question or not question.strip():
		return QueryResult(question=question, answer="", citations=[], retrieved_chunks=0)

	query_bundle = QueryBundle(query_str=question)
	try:
		source_nodes = retriever._retrieve(query_bundle)
	except Exception:
		# Fall back to empty result on retrieval errors
		source_nodes = []

	citable_nodes, citations = prepare_citation_context(source_nodes)

	answer_body = _join_citable_texts(citable_nodes[:8])
	sources = format_citations(citations)

	if sources:
		answer_text = f"{answer_body}\n\n{sources}" if answer_body else sources
	else:
		answer_text = answer_body or "I could not find relevant sources for that question."

	return QueryResult(
		question=question,
		answer=answer_text,
		citations=citations,
		retrieved_chunks=len(source_nodes),
	)


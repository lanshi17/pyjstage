from typing import Dict, Optional, List
import re
from datetime import datetime
from .entry import ListEntry, SearchEntry
from lxml import etree

def _safe_text(el, default=''):
    """Extract text from an element, handling None and empty tags."""
    if el is None:
        return default
    text = el.text
    return text.replace('\n', '').strip() if text else default


def _safe_int(el, default=0):
    """Extract integer from an element, handling None/empty/non-numeric."""
    text = _safe_text(el)
    if not text:
        return default
    try:
        return int(text)
    except (ValueError, TypeError):
        return default


def _lang_dict(parent, xmlns):
    """Build {lang: text} dict from child elements, handling empty tags."""
    if parent is None:
        return {}
    regex = re.compile(r'{.+\}')
    return {
        regex.sub('', t.tag): _safe_text(t)
        for t in parent
    }


class Result:
    """Base class for Result
    Attributes:
        encoding: Document encoding, it may always be utf-8.
        xml_version: XML version.
        xmlns: What namespaces does this document refer.
        xml_lang: What language is this document written in.
        status: Status code.
        message: Status message.
        title: returned title
        link: returned link
        id: document id, it is always same as link value.
        servicecd: API service code, 2 is list and 3 is search.
        updated: When was this document updated.
        total_results: How many results did API return.
        start_index: What index do results starts.
        items_per_page: How many items does a page contain.
        entries: Entries API returned.
    """
    def __init__(self):
        self.encoding: Optional[str] = None
        self.xml_version: Optional[str] = None
        self.xmlns: Dict[str, str] = {}
        self.xml_lang: Optional[str] = None
        self.status: str = Optional[None]
        self.message: Optional[str] = None
        self.title: Optional[str] = None
        self.link: Optional[str] = None
        self.id: Optional[str] = None
        self.servicecd: Optional[str] = None
        self.updated: Optional[datetime] = None
        self.total_results: Optional[int] = None
        self.start_index: Optional[int] = None
        self.items_per_page: Optional[int] = None
        self.entries: List[etree] = []
        self.entries_temp: List[etree] = []

    def _finish_setup(self):
        """remove unused temporary attribute"""
        del self.entries_temp

    def __str__(self):
        return str(self.__dict__.items())


class SearchResult(Result):
    """Search Result Class

    Attributes:
        encoding: Document encoding, it may always be utf-8.
        xml_version: XML version.
        xmlns: What namespaces does this document refer.
        xml_lang: What language is this document written in.
        status: Status code.
        message: Status message.
        title: returned title
        link: returned link
        id: document id, it is always same as link value.
        servicecd: API service code, 2 is list and 3 is search.
        updated: When was this document updated.
        total_results: How many results did API return.
        start_index: What index do results starts.
        items_per_page: How many items does a page contain.
        entries: Entries API returned.
    """
    def __init__(self, result: Result):
        """Initialize SearchResult class

        Args:
            result: Result object
        """
        super().__init__()
        self.encoding = result.encoding
        self.xml_version = result.xml_version
        self.xmlns = result.xmlns
        self.xml_lang = result.xml_lang
        self.status = result.status
        self.message = result.message
        self.title = result.title
        self.link = result.link
        self.id = result.id
        self.servicecd = result.servicecd
        self.updated = result.updated
        self.total_results = result.total_results
        self.start_index = result.start_index
        self.items_per_page = result.items_per_page
        self.entries_temp = result.entries
        self.entries = []

        for e in self.entries_temp:
            ent = SearchEntry()
            ent.article_title = _lang_dict(e.find('./article_title', self.xmlns), self.xmlns)
            ent.article_link = _lang_dict(e.find('./article_link', self.xmlns), self.xmlns)
            author_el = e.find('./author', self.xmlns)
            if author_el is not None:
                ent.author = {}
                regex = re.compile(r'{.+\}')
                for t in author_el:
                    children = list(t)
                    ent.author[regex.sub('', t.tag)] = _safe_text(children[0]) if children else ''
            else:
                ent.author = {}
            ent.cdjournal = _safe_text(e.find('./cdjournal', self.xmlns))
            ent.material_title = _lang_dict(e.find('./material_title', self.xmlns), self.xmlns)
            ent.issn = _safe_text(e.find('./prism:issn', self.xmlns))
            ent.eissn = _safe_text(e.find('./prism:eIssn', self.xmlns))
            ent.volume = _safe_int(e.find('./prism:volume', self.xmlns))
            ent.number = _safe_int(e.find('./prism:number', self.xmlns))
            ent.starting_page = _safe_text(e.find('./prism:startingPage', self.xmlns))
            ent.ending_page = _safe_text(e.find('./prism:endingPage', self.xmlns))
            ent.pubyear = _safe_text(e.find('./pubyear', self.xmlns))
            ent.doi = _safe_text(e.find('./prism:doi', self.xmlns))
            ent.systemcode = _safe_int(e.find('./systemcode', self.xmlns))
            ent.systemname = _safe_text(e.find('./systemname', self.xmlns))
            ent.title = _safe_text(e.find('./title', self.xmlns))
            link_el = e.find('./link', self.xmlns)
            ent.link = (link_el.attrib.get('href', '').replace('\n', '').strip()) if link_el is not None else ''
            ent.id = _safe_text(e.find('./id', self.xmlns))
            updated_text = _safe_text(e.find('./updated', self.xmlns))
            ent.updated = datetime.fromisoformat(updated_text) if updated_text else None
            self.entries.append(ent)
        self._finish_setup()


class ListResult(Result):
    """List Result Class

    Attributes:
        encoding: Document encoding, it may always be utf-8.
        xml_version: XML version.
        xmlns: What namespaces does this document refer.
        xml_lang: What language is this document written in.
        status: Status code.
        message: Status message.
        title: returned title
        link: returned link
        id: document id, it is always same as link value.
        servicecd: API service code, 2 is list and 3 is search.
        updated: When was this document updated.
        total_results: How many results did API return.
        start_index: What index do results starts.
        items_per_page: How many items does a page contain.
        entries: Entries API returned.
    """
    def __init__(self, result: Result = None):
        """Initialize ListResult class

        Args:
            result: Result object
        """
        super().__init__()
        self.encoding = result.encoding
        self.xml_version = result.xml_version
        self.xmlns = result.xmlns
        self.xml_lang = result.xml_lang
        self.status = result.status
        self.message = result.message
        self.title = result.title
        self.link = result.link
        self.id = result.id
        self.servicecd = result.servicecd
        self.updated = result.updated
        self.total_results = result.total_results
        self.start_index = result.start_index
        self.items_per_page = result.items_per_page
        self.entries_temp = result.entries
        self.entries = []

        for e in self.entries_temp:
            ent = ListEntry()
            ent.vols_title = _lang_dict(e.find('./vols_title', self.xmlns), self.xmlns)
            ent.vols_link = _lang_dict(e.find('./vols_link', self.xmlns), self.xmlns)
            ent.issn = _safe_text(e.find('./prism:issn', self.xmlns))
            ent.eissn = _safe_text(e.find('./prism:eIssn', self.xmlns))
            ent.publisher_name = _lang_dict(e.find('./publisher/name', self.xmlns), self.xmlns)
            ent.publisher_url = _lang_dict(e.find('./publisher/url', self.xmlns), self.xmlns)
            ent.cdjournal = _safe_text(e.find('./cdjournal', self.xmlns))
            ent.material_title = _lang_dict(e.find('./material_title', self.xmlns), self.xmlns)
            ent.volume = _safe_int(e.find('./prism:volume', self.xmlns))
            ent.number = _safe_int(e.find('./prism:number', self.xmlns))
            ent.starting_page = _safe_int(e.find('./prism:startingPage', self.xmlns))
            ent.pubyear = _safe_text(e.find('./pubyear', self.xmlns))
            ent.systemcode = _safe_int(e.find('./systemcode', self.xmlns))
            ent.systemname = _safe_text(e.find('./systemname', self.xmlns))
            ent.title = _safe_text(e.find('./title', self.xmlns))
            link_el = e.find('./link', self.xmlns)
            ent.link = (link_el.attrib.get('href', '').replace('\n', '').strip()) if link_el is not None else ''
            ent.id = _safe_text(e.find('./id', self.xmlns))
            updated_text = _safe_text(e.find('./updated', self.xmlns))
            ent.updated = datetime.fromisoformat(updated_text) if updated_text else None
            self.entries.append(ent)
        self._finish_setup()

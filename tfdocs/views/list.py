from textual.widgets import OptionList

class List(OptionList, can_focus=False):
    DEFAULT_CSS = """
        List {
            background: transparent;
            padding: 0;
            margin: 0;
            scrollbar-size: 1 1;
        }

		.option-list--option-highlighted {
			background: $boost !important;
		}
    """

    def __init__(self, resources, id=None):
        if id != None:
            super().__init__(*resources, id=id)
        else:
            super().__init__(*resources)

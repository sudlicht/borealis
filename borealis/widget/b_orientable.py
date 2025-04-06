from borealis.widget.enums import Orientation


class B_Orientable:
    """
    An extra class which should be added to borealis abstracted
    versions of classes which implement Orientable from Gtk.

    Adds b_ prefixed versions of orientable methods which support
    borealis orientation.
    """

    orientation: Orientation = Orientation.HORIZONTAL
    """
    The orientation of the box, this is the plane of
    which the children will be in
    """

    def b_set_orientation(self, orientation: Orientation):
        """
        Set's the orientation of this box to a certain orientation

        Args:
            orientation (Orientation): The new orientation of the box
        """
        self.set_orientation(orientation.value)

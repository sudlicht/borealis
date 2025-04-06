import copy
import logging

logger = logging.getLogger(__name__)


class CopyWidget:
    """
    Special class for allowing re-initialisation of widgets/
    copying them so they can unique per instance,

    Only applies if a widget has more than once instance
    """

    instances: dict[object, bool] = {}
    """
    The amount of instances tracker for each widget
    """

    def _reinitialise_widget(self) -> "CopyWidget":
        """
        Reinitialises this widget, returning a new copy
        """

        # No more than one instance of this widget
        if id(self) not in CopyWidget.instances:
            CopyWidget.instances[id(self)] = 1
            return self

        attrs = self.__dict__
        copied_attrs = {}

        # Reinitialise all of the attributes
        for attr_name, attr_value in attrs.items():
            copied_attrs[attr_name] = self._copy_field(attr_value)

        return self.__class__(**copied_attrs)

    def _copy_field(self, value: any) -> any:
        """
        Copies a single field, returning the new value of the field

        Args:
            value (any): The value of the field
        """
        new_value = None

        if isinstance(value, list):
            # Copy list
            new_value = []

            for sub_value in value:
                new_value.append(self._copy_field(sub_value))

        elif isinstance(value, CopyWidget):
            # Copy widget
            new_value = value._reinitialise_widget()

        elif isinstance(value, dict):
            # Copy dict
            new_value = {}

            for key, sub_value in value.items():
                new_value[key] = self._copy_field(sub_value)

        else:
            try:
                new_value = copy.deepcopy(value)
            except TypeError as e:
                logger.critical(
                    f"Failed to copy field with value {value} due to exception: {e}"
                )

        return new_value

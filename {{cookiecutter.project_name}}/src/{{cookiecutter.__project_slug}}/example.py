"""Behold, module level docstring."""


class Example:
    """This class exists to show off autodocstring generation."""

    def add(self, a: int, b: int) -> int:
        """Add two integers.

        Notes:
            Docstring can be useful. I promise.

        Parameters:
            a: First integer to add.
            b: Second integer to add.

        Returns:
            The sum of the two integers.
        """
        return a + b

    def subtract(self, a: int, b: int) -> int:
        """Subtract two integers.

        Parameters:
            a: Integer to subtract from.
            b: Integer to subtract.

        Returns:
            The difference of the two integers.
        """
        return a - b

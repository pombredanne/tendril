## Copyright (C) 2012 by Kevin L. Mitchell <klmitch@mit.edu>
##
## This program is free software: you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see
## <http://www.gnu.org/licenses/>.

import abc


class Application(object):
    """
    Base class for tracking application state.  Application classes
    are responsible for implementing the base methods documented here.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, parent):
        """
        Initialize the Application.
        """

        self.parent = parent

    def close(self):
        """
        Close the connection.
        """

        self.parent.close()

    def send_frame(self, frame):
        """
        Send a frame across a connection.
        """

        self.parent.send_frame(frame)

    @abc.abstractmethod
    def closed(self, error):
        """
        Called to notify the application that the connection has been
        closed.  Not called if the application initiates the closure.

        :param error: The exception resulting in the connection
                      closure.  If the closure is due to an EOF
                      condition, will be ``None``.
        """

        pass

    @abc.abstractmethod
    def recv_frame(self, frame):
        """
        Called to pass received frames to the application.
        """

        pass
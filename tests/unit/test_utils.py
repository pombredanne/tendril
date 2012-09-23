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

import unittest

import mock

from tendril import utils


class TestTendrilPartial(unittest.TestCase):
    def test_init(self):
        partial = utils.TendrilPartial('func', 1, 2, 3, a=4, b=5, c=6)

        self.assertEqual(partial.func, 'func')
        self.assertEqual(partial.args, (1, 2, 3))
        self.assertEqual(partial.kwargs, dict(a=4, b=5, c=6))

    def test_call(self):
        func = mock.Mock(return_value="result")
        partial = utils.TendrilPartial(func, 1, 2, 3, a=4, b=5, c=6)
        result = partial("arg1", "arg2", "arg3")

        self.assertEqual(result, "result")
        func.assert_called_once_with("arg1", "arg2", "arg3", 1, 2, 3,
                                     a=4, b=5, c=6)


class TestWrapperChain(unittest.TestCase):
    def test_init(self):
        chain = utils.WrapperChain()

        self.assertEqual(chain._wrappers, [])

    def test_init_wrapper(self):
        chain = utils.WrapperChain('wrapper')

        self.assertEqual(chain._wrappers, ['wrapper'])

    @mock.patch.object(utils, 'TendrilPartial',
                       new=lambda func, *args, **kwargs: (func, args, kwargs))
    def test_init_wrapper_args(self):
        chain = utils.WrapperChain('wrapper', 1, 2, 3, a=4, b=5, c=6)

        self.assertEqual(chain._wrappers, [
                ('wrapper', (1, 2, 3), dict(a=4, b=5, c=6)),
                ])

    @mock.patch.object(utils, 'TendrilPartial',
                       new=lambda func, *args, **kwargs: (func, args, kwargs))
    def test_chain(self):
        # chain() has already been tested during the tests of
        # __init__() above, so we need merely do one last double-check
        # and test the convenience return
        chain = utils.WrapperChain()

        result = chain.chain('wrapper', 1, 2, 3, a=4, b=5, c=6)

        self.assertEqual(id(chain), id(result))
        self.assertEqual(chain._wrappers, [
                ('wrapper', (1, 2, 3), dict(a=4, b=5, c=6)),
                ])

    def test_call(self):
        chain = utils.WrapperChain(mock.Mock(return_value="sock2"))\
            .chain(mock.Mock(return_value="sock3"))\
            .chain(mock.Mock(return_value="sock4"))

        result = chain("sock1")

        self.assertEqual(result, "sock4")
        chain._wrappers[0].assert_called_once_with("sock1")
        chain._wrappers[1].assert_called_once_with("sock2")
        chain._wrappers[2].assert_called_once_with("sock3")
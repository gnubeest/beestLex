###
# Copyright (c) 2020, Brian McCord
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import requests

from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('BeestLex')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class BeestLex(callbacks.Plugin):
    """dictionary"""
    pass


    def lex(self, irc, msg, args, input_word):
        """[<word>]
            Get definitions for <word>.
        """

        mw_api = self.registryValue("MWKey")
        dict_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
        payload = {'key': mw_api}
        pink = "\x0313"
        green = "\x0303"
        nulattr = "\x0F"

        dict_d = (requests.get(dict_url + input_word, params = payload)).json()
        full_def = ''
        reply_build = ''

        # add cognate redirection for silly American dictionary
        try:
            cognate = dict_d[0]['cxs'][0]
            reply_build = (pink + (dict_d[0]['hwi']['hw']).replace("*", "") +
                nulattr + ": \x1D" + cognate['cxl'] + nulattr + " ")
            dict_d = (requests.get(dict_url + cognate['cxtis'][0]['cxt'],
                params = payload)).json()
        except (KeyError, IndexError, TypeError):
            pass

        # okay we'll try to get some short definitions
        try:
            for i in range(0, 20):
                headword = (pink + "\x02" +
                    (dict_d[i]['hwi']['hw']).replace("*", "") + nulattr)
                func_lab = (green + " \x1D" + str(dict_d[i]['fl']) + nulattr
                    + green + " " + str(i + 1) + nulattr)
                homo_def = (dict_d[i]['shortdef'])
                def_1 = def_2 = def_3 = ''
                try:
                    def_1 = green + ": " + nulattr + homo_def[0]
                    def_2 = "; " + green + str(i + 1) + "b: " + nulattr + homo_def[1]
                    def_3 = "; " + green + str(i + 1) + "c: " + nulattr + homo_def[2]
                except IndexError:
                    pass
                # cut down on upstream "imitative" entries
                #if def_3 == def_2:
                #    def_3 = ''
                #if def_2 == def_1:
                #    def_2 == ''
                reply_build = reply_build + green + "▶" + (headword +
                    func_lab + def_1 + def_2 + def_3) + " "
        except (KeyError, IndexError):
            pass
        # halp cannot speel
        except TypeError:
            try:
                irc.reply(green + 'Did you mean ' + pink + dict_d[0] + ", " +
                    dict_d[1] + ", " + dict_d[2] + green + "?")
            except IndexError:
                irc.reply(green + 'Did you mean ' + pink + dict_d[0] + green
                    + "?")
            return

        # what is this I can't even
        if reply_build == '':
            irc.reply("I can't find a word or suggestion for " + pink +
                input_word + nulattr + ".")
        else:
            irc.reply(reply_build, prefixNick=False)

    lex = wrap(lex, ['something'])

Class = BeestLex


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

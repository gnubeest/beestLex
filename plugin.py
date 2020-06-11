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

pink = "\x0313"
green = "\x0303"
nulattr = "\x0F"
bullet = " \x0303•\x0f "

class BeestLex(callbacks.Plugin):
    """IRC-legible dictionary"""
    pass


    def syn(self, irc, msg, args, input_word):
        """[<input>]
            Get English synonyms for <input>.
        """

        if input_word == "":
            irc.error('Received null input')
            return

        mw_api = self.registryValue("MWThesKey")
        syn_url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"
        payload = {'key': mw_api}
        syn_d = (requests.get(syn_url + input_word, params=payload)).json()

        try:
            syn_test = syn_d[0]['meta']['syns']
        except TypeError:
            syn_cog = syn_d[0]
            syn_d = (requests.get(syn_url + syn_cog, params=payload)).json()
        except NameError:
            irc.reply("I can't find synonyms for " + pink +
                      input_word + nulattr + ".")
            return


        def syn_bld(in_word):
            syn_out = ''
            for idx in range(0, 10):
                try:
                    hword = (pink + '\x02' + syn_d[idx]['hwi']['hw'] + nulattr)
                    syn_def = syn_d[idx]['shortdef'][0]
                    syn_lst = syn_d[idx]['meta']['syns'][0]
                    syn_lst = ', '.join(syn_lst)
                    syn_out = (syn_out + green + '▶' + hword + green +
                               " \x1D" + syn_def + " " + nulattr + syn_lst + " ")
                except IndexError:
                    pass
            return syn_out 

        syn_print = syn_bld(syn_d)
        irc.reply(syn_print)


    syn = wrap(syn, ['text'])





    def lex(self, irc, msg, args, input_word):
        """[<input>]
            Get English definitions for <input>.
        """

        if input_word == "":
            irc.error('Received null input')
            return

        mw_api = self.registryValue("MWKey")
        dict_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
        payload = {'key': mw_api}

        dict_d = (requests.get(dict_url + input_word, params=payload)).json()
        reply_build = ''

        # automatic redirection
        try:
            cognate = dict_d[0]['cxs'][0]
            reply_build = (pink + (dict_d[0]['hwi']['hw']).replace("*", "") +
                           nulattr + ": \x1D" + cognate['cxl'] + nulattr + " ")
            dict_d = (requests.get(dict_url + cognate['cxtis'][0]['cxt'],
                                   params=payload)).json()
        except (KeyError, IndexError, TypeError):
            pass

        # okay we'll try to get some definitions
        try:
            for i in range(0, 20):
                headword = (pink + "\x02" +
                            (dict_d[i]['hwi']['hw']).replace("*", "") + nulattr)
                homo_def = (dict_d[i]['shortdef'])
                # main entry, status labels
                homo_sls1 = homo_sls2 = ''
                try:
                    homo_sls1 = ", " + (dict_d[i]['def'][0]['sseq'][0][0][1]
                                        ['sls'][0])
                    homo_sls2 = ", " + (dict_d[i]['def'][0]['sseq'][0][0][1]
                                        ['sls'][1])
                except (KeyError, TypeError, IndexError):
                    pass
                func_lab = (green + " \x1D" + str(dict_d[i]['fl']) +
                            homo_sls1 + homo_sls2 + nulattr + green + " " +
                            str(i + 1))
                # B status labels
                sls_b1 = sls_b2 = ''
                try:
                    sls_b1 = "\x1D " + (dict_d[i]['def'][0]['sseq'][1][0][1]
                                        ['sls'][0])
                    sls_b2 = ", " + (dict_d[i]['def'][0]['sseq'][1][0][1]
                                     ['sls'][1])
                except:
                    pass
                # C status labels
                sls_c1 = sls_c2 = ''
                try:
                    sls_c1 = "\x1D " + (dict_d[i]['def'][0]['sseq'][2][0][1]
                                        ['sls'][0])
                    sls_c2 = ", " + (dict_d[i]['def'][0]['sseq'][2][0][1]
                                     ['sls'][1])
                except:
                    pass
                # build an entry set
                def_1 = def_2 = def_3 = ''
                try:
                    def_1 = ": " + nulattr + homo_def[0]
                    def_2 = ("; " + green + str(i + 1) + "b:" + sls_b1 +
                             sls_b2 + " " + nulattr + homo_def[1])
                    def_3 = ("; " + green + str(i + 1) + "c:" + sls_c1 +
                             sls_c2 + " " + nulattr + homo_def[2])
                except IndexError:
                    pass
                reply_build = (reply_build + green + "▶" + headword +
                               func_lab + def_1 + def_2 + def_3 + " ")
        except (KeyError, IndexError):
            pass
        # halp cannot speel, maek suggest
        except TypeError:
            irc.reply(green + 'Did you mean: ' + pink +
                      ((str(dict_d)).translate
                      (str.maketrans({',': '', '[': '', ']': ''}))))
            return

        # can't do anything with silly user's input
        if reply_build == '':
            irc.reply("I can't find a word or suggestion for " + pink +
                      input_word + nulattr + ".")
        # if there's a definition, show it
        else:
            irc.reply(reply_build, prefixNick=False)

    lex = wrap(lex, ['text'])

Class = BeestLex


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

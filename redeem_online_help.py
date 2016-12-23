from errbot import BotPlugin, botcmd, cmdfilter
import sys
import os
import importlib
import inspect


class RedeemOnlineHelp(BotPlugin):
    def __init__(self, *args, **kwargs):
        super(RedeemOnlineHelp, self).__init__(*args, **kwargs)
        redeem_path = getattr(self.bot_config, 'REDEEM_PATH', None)
        redeem_path_gcodes = os.path.join(redeem_path, 'gcodes')

        self.redeem_path = redeem_path
        self.redeem_path_gcodes = redeem_path_gcodes

        try:
            sys.path.append(self.redeem_path)
            sys.path.append(self.redeem_path_gcodes)
            importlib.import_module('M119')
            self.redeem_load_error = False
        except ImportError:
            self.log.info("RedeemOnlineHelp: Cannot load redeem modules.")
            self.redeem_load_error = True

        self.gcodes = {}

        try:
            modules = os.listdir(self.redeem_path_gcodes)
        except FileNotFoundError:
            self.log.info("RedeemOnlineHelp: Redeem path not found.")
            self.redeem_load_error = True

        if self.redeem_load_error:
            return

        except_list = ['Deprecated_commands.py',
                       '__init__.py']

        for mod in modules:
            if not mod.endswith('.py') or mod in except_list:
                continue

            try:
                imp_mod = importlib.import_module(mod.replace('.py', ''))
            except Exception as e:
                imp_mod = None
                self.log.info(
                    "RedeemOnlineHelp: failed to load class {}: {}".format(
                        mod,
                        e)
                )

            if not imp_mod:
                continue

            for member in dir(imp_mod):
                mod_ref = getattr(imp_mod, member)

                if (member in ['ToolChange', 'GCodeCommand'] or
                        not inspect.isclass(mod_ref) or
                        not issubclass(mod_ref, imp_mod.GCodeCommand)):
                    continue

                try:
                    desc = mod_ref.get_description(imp_mod)
                except AttributeError:
                    desc = None

                self.gcodes[member.lower()] = {
                    'desc': desc
                }

    @botcmd
    def gcode(self, msg, args):
        if not self.redeem_path or self.redeem_load_error:
            return "Sorry, but the redeem path is not configured correctly."

        if not len(args):
            msg = (", ").join(self.gcodes.keys())
            return "(RedeemOnlineHelp) gcode help: " + msg

        if args.lower() in self.gcodes:
            reply = "{code}: {desc}".format(
                code=args.lower(),
                desc=self.gcodes[args.lower()]['desc']
            )
            return "(RedeemOnlineHelp) " + reply

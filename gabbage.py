usage = "usage: %prog [options]"
parser = OptionParser(usage)
parser.add_option("-b", "--displayHeartbeat", dest = "verbose", action = "store_true",
                  help = "Display HeartBeat in streaming data")
self.displayHeartbeat = False

(options, args) = parser.parse_args()
if len(args) > 1:
  parser.error("incorrect number of arguments")
if options.verbose:
  self.displayHeartbeat = True

  リミットオーダーは決済の指値注文を、ストップオーダーは決済の逆指値注文を、トレーリングストップは決済の自動修正付き逆指値注文を指します。

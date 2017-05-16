#!/usr/bin/env python

#-*- encoding: utf-8 -*-
import sys
import os
import tornado.ioloop

__author__ = "Krzysztof Wesolowski"
__license__ = "LGPLv3"
__maintainer__ = "Krzysztof Wesolowski"
__copyright__ = "Copyleft by Wolnosciowiec Team"

t = sys.argv[0].replace(os.path.basename(sys.argv[0]), "") + "/../src/"

if os.path.isdir(t):
    sys.path.append(t)

import Deployer
from tornado.options import options

if __name__ == "__main__":
    app = Deployer.create_application()
    app.listen(options.port, options.listen)

    tornado.ioloop.IOLoop.current().start()

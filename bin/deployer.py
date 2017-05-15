#!/usr/bin/env python

#-*- encoding: utf-8 -*-
import sys
import os
import tornado.ioloop

__author__ = "Krzysztof Wesołowski"
__license__ = "LGPLv3"
__maintainer__ = "Krzysztof Wesołowski"
__copyright__ = "Copyleft by Wolnościowiec Team"

t = sys.argv[0].replace(os.path.basename(sys.argv[0]), "") + "/../src/"

if os.path.isdir(t):
    sys.path.append(t)

import Deployer

if __name__ == "__main__":
    app = Deployer.create_application()
    app.listen(8012)
    tornado.ioloop.IOLoop.current().start()

# encoding: UTF-8
# Copyright 2017 Google.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tensorflow as tf
import numpy as np
import my_txtutils
import argparse

# these must match what was saved !
ALPHASIZE = my_txtutils.ALPHASIZE
NLAYERS = 3
INTERNALSIZE = 512




parser = argparse.ArgumentParser()
parser.add_argument("checkpoint", help="The checkpoint for the training run to be used for generation");
parser.add_argument("-i", "--internalsize", dest="internalsize", help="Internal size", type=int, default=512)
parser.add_argument("-n", "--nlayers", dest="nlayers", help="Number of layers", type=int, default=3)
parser.add_argument("-t", "--topn", type=int, 
   dest="topn", help="topn value for generation", default=2)
parser.add_argument("-l", "--length", type=int, 
   dest="length", help="number of characters to be created", default=1000000)
args = parser.parse_args()

INTERNALSIZE = args.internalsize
NLAYERS = args.nlayers

# use topn=10 for all but the last one which works with topn=2 for Shakespeare and topn=3 for Python

base = args.checkpoint.split("-")[0]

author = 'checkpoints/' + args.checkpoint
meta = author + '.meta'


ncnt = 0
with tf.Session() as sess:
    new_saver = tf.train.import_meta_graph(meta)
    new_saver.restore(sess, author)
    x = my_txtutils.convert_from_alphabet(ord("L"))
    x = np.array([[x]])  # shape [BATCHSIZE, SEQLEN] with BATCHSIZE=1 and SEQLEN=1

    # initial values
    y = x
    h = np.zeros([1, INTERNALSIZE * NLAYERS], dtype=np.float32)  # [ BATCHSIZE, INTERNALSIZE * NLAYERS]
    for i in range(args.length):
        yo, h = sess.run(['Yo:0', 'H:0'], feed_dict={'X:0': y, 'pkeep:0': 1., 'Hin:0': h, 'batchsize:0': 1})

        # If sampling is be done from the topn most likely characters, the generated text
        # is more credible and more "english". If topn is not set, it defaults to the full
        # distribution (ALPHASIZE)

        # Recommended: topn = 10 for intermediate checkpoints, topn=2 or 3 for fully trained checkpoints

        c = my_txtutils.sample_from_probabilities(yo, topn=int(args.topn))
        y = np.array([[c]])  # shape [BATCHSIZE, SEQLEN] with BATCHSIZE=1 and SEQLEN=1
        c = chr(my_txtutils.convert_to_alphabet(c))
        print(c, end="")

        if c == '\n':
            ncnt = 0
        else:
            ncnt += 1
        if ncnt == 100:
            print("")
            ncnt = 0


#         TITUS ANDRONICUS
#
#
# ACT I
#
#
#
# SCENE III	An ante-chamber. The COUNT's palace.
#
#
# [Enter CLEOMENES, with the Lord SAY]
#
# Chamberlain	Let me see your worshing in my hands.
#
# LUCETTA	I am a sign of me, and sorrow sounds it.
#
# [Enter CAPULET and LADY MACBETH]
#
# What manner of mine is mad, and soon arise?
#
# JULIA	What shall by these things were a secret fool,
# That still shall see me with the best and force?
#
# Second Watchman	Ay, but we see them not at home: the strong and fair of thee,
# The seasons are as safe as the time will be a soul,
# That works out of this fearful sore of feather
# To tell her with a storm of something storms
# That have some men of man is now the subject.
# What says the story, well say we have said to thee,
# That shall she not, though that the way of hearts,
# We have seen his service that we may be sad.
#
# [Retains his house]
# ADRIANA	What says my lord the Duke of Burgons of Tyre?
#
# DOMITIUS ENOBARBUS	But, sir, you shall have such a sweet air from the state,
# There is not so much as you see the store,
# As if the base should be so foul as you.
#
# DOMITIUS ENOY	If I do now, if you were not to seek to say,
# That you may be a soldier's father for the field.
#
# [Exit]

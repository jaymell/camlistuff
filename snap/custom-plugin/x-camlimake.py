import snapcraft
import glob
import os
import shutil

class Camlimake(snapcraft.BasePlugin):

  def build(self):
    super().build()
    print('Building camlistore...')
    self.run(['go', 'run', 'make.go'])

    for i in glob.glob(os.path.join(self.builddir, 'bin/*')):
      source = i
      destination = os.path.join(self.installdir, 'bin', os.path.basename(i))
      print("Source: %s" % source)
      print("Destination: %s" % destination)
      if not os.path.exists(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination), exist_ok=True)
      shutil.copy2(source, destination)

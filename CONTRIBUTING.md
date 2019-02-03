# Contributing to Sledge (Draft)  
Sledge is an open source project so we always welcome your ideas, and appreciate your efforts in trying to make Sledge a better project for the community.  
Before contributing to this repository, you must have discussed the changes you wish to make and things you wish to add, via email, github issue template for our repo or any other effective method, with the administrator or owners of Sledge.  
You are advised to follow our [CODE-OF-CONDUCT](https://github.com/framestd/sledge/tree/master/CODE-OF-CONDUCT.md) as a guide to any interactions you make with/on this repository.  
## Issue tracker  
The [issue tracker](https://github.com/framestd/sledge/issues) is the channel for [bugs reports](#bug-reports), [feature request](feature-request) on Sledge.  
## Pull Request Process  
1. To engage in the pull request process, you may [fork](https://help.github.comarticles/fork-a-repo/) our repo, clone the repo you forked and using your git software configure remote handling of the repo you cloned from the fork.  
  ```bash
  # after the fork
  git clone https://github.com/<your-username>/sledge.git
  # after clone
  cd sledge
  # add upstream
  git remote add upstream https://github.com/framestd/sledge.git

  # if it's been a while you cloned, update
  git checkout master
  git pull upstream master
  ```  

2. Create a new topic branch to contain your changes or fix
  ```bash
  git checkout -b <topic-branch-name>
  ```  
3. Commit changes bit by bit recording what changes you made with your commit message. Do not commit a whole lot of cahnges at once except it is a similar change in all. Follow this [commit guidelines](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)  
4. Merge or rebase the upstream dev branch into your topic branch
  ```bash
  git pull [--rebase] upstream master
  ```  
5. Push your topic branch to your fork
  ```bash
  git push origin <topic-branch-name>
  ```  
6. [Open a Pull Request](https://help.github.com/articles/about-pull-request/) with a resonable title and description against the master branch.  
**NOTE**: submitting your work makes us believe that you agree to license your work under the same [license of this project](https://github.com/framestd/sledge/tree/master/LICENSE)  

**By submitting your work you assure us you ensured the following**:
1. You removed install or build dependencies.  
2. You update the README.md, and in a very concise and comprehensible language, described for the changes you made: things pertaining to usage, what to use, what not to use, if required code snippet for usage.  
3. This project follows the Semantic Versioning rules major.minor.patch. Update/Increase the version number wherever required, and follow the versioning rules and regulations defined at [Semver.org](https://www.semver.org): Backwards incompatible API changes would cause a bump in the major, backwards compatible changes should cause a bump in the minor, bug fixes would cause a bump in the patch. Although we do not allow API changes so changes can only cause bump in either minor or patch.  
4. You must have edited the docs to document changes. **Do not edit &asterisk;.html files in the docs folder, instead edit the &asterisk;.rm files in the remarkup directory, edit similar panes in the panes directory and build using this same software you are about to submit.**  
5. You must have tested your work and see that it works as desired.

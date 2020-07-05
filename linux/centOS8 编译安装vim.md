# centos7下编译安装vim8

    git clone https://github.com/vim/vim.git

    cd vim
    cd src

## 设置,检查环境

    ./configure --with-features=huge \
    --enable-multibyte \
    --enable-rubyinterp=yes \
    --enable-pythoninterp=yes \
    --enable-python3interp=yes \
    --prefix=/usr/local/vim8

### 提示错误

    checking for tgetent in -lcurses... no
    no terminal library found
    checking for tgetent()... configure: error: NOT FOUND!
        You need to install a terminal library; for example ncurses.
        Or specify the name of the library with --with-tlib.

安装ncurses-devel

    sudo yum install ncurses-devel

### 注意：若重新设置，需运行```make distclean```

## 编译安装

    make
    sudo make install
    sudo ln -s /usr/local/vim8 /usr/bin/vim

## 插件安装

### 安装vundle

    git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim

设置插件，在.vimrc增加插件信息

    " vundle 环境设置
    filetype off
    set rtp+=~/.vim/bundle/Vundle.vim
    " vundle 管理的插件列表必须位于 vundle#begin() 和 vundle#end() 之间
    call vundle#begin()
    Plugin 'VundleVim/Vundle.vim'
    Plugin 'altercation/vim-colors-solarized'
    Plugin 'tomasr/molokai'
    Plugin 'vim-scripts/phd'
    Plugin 'Lokaltog/vim-powerline'
    Plugin 'octol/vim-cpp-enhanced-highlight'
    Plugin 'nathanaelkane/vim-indent-guides'
    Plugin 'derekwyatt/vim-fswitch'
    Plugin 'kshenoy/vim-signature'
    Plugin 'vim-scripts/BOOKMARKS--Mark-and-Highlight-Full-Lines'
    Plugin 'majutsushi/tagbar'
    Plugin 'vim-scripts/indexer.tar.gz'
    Plugin 'vim-scripts/DfrankUtil'
    Plugin 'vim-scripts/vimprj'
    Plugin 'dyng/ctrlsf.vim'
    Plugin 'terryma/vim-multiple-cursors'
    Plugin 'scrooloose/nerdcommenter'
    Plugin 'vim-scripts/DrawIt'
    Plugin 'SirVer/ultisnips'
    Plugin 'Valloric/YouCompleteMe'
    Plugin 'derekwyatt/vim-protodef'
    Plugin 'scrooloose/nerdtree'
    Plugin 'fholgado/minibufexpl.vim'
    Plugin 'gcmt/wildfire.vim'
    Plugin 'sjl/gundo.vim'
    Plugin 'Lokaltog/vim-easymotion'
    Plugin 'suan/vim-instant-markdown'
    Plugin 'lilydjwg/fcitx.vim'
    " 插件列表结束
    call vundle#end()
    filetype plugin indent on

进入vim执行```:PluginInstall```

### Ycmd安装

错误提示：

    The ycmd server SHUT DOWN (restart with ':YcmRestartServer').

1. 进入YCM插件目录

    cd ~/.vim/bundle/YouCompleteMe/

2. 执行安装

    python3 install.py

### vundle管理

卸载插件

1. .vimrc中注释插件信息
2. vim中执行```:PluginClean```

更新插件
```:PluginUpdate```

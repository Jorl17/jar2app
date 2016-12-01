# jar2app

**jar2app** is a Python 2/3 script that can easily convert any *jar* file into a *Mac OS X app* file. It seeks **simplicity**, and in fact can be run just like

    jar2app input.jar
    
creating `input.App` in the process. No third-party libraries. No cruft.

Though simple and easy to use, there are **loads of configurable options**, such as setting icons, bundle names or bundling your own JRE/JDK.

**Install instructions** can be found [here](#how-do-i-installuninstall-it). **Example usage** can be found [here](#example-usage).

It should run in any operating system (Windows, Mac OS X, Linux), but of course you'll only test the results in a Mac OS X system.

Table of Contents
=================

  * [Aren't there other tools that do this? Why another one?](#arent-there-other-tools-that-do-this-why-another-one)
  * [Can I submit bundles created with jar2app to the Appstore?](#can-i-submit-bundles-created-with-jar2app-to-the-appstore)
  * [How do I install/uninstall it?](#how-do-i-installuninstall-it)
    * [Examples:](#examples)
      * [Install](#install)
      * [Install to /usr/local/bin prefix](#install-to-usrlocalbin-prefix)
      * [Uninstall](#uninstall)
      * [Uninstall from /usr/local/bin prefix](#uninstall-from-usrlocalbin-prefix)
  * [How does it work?](#how-does-it-work)
  * [What exactly can I change?](#what-exactly-can-i-change)
  * [Does jar2app bundle its own JRE/JDK? Can I bundle my own?](#does-jar2app-bundle-its-own-jrejdk-can-i-bundle-my-own)
  * [Does jar2app figure the main class of my jar automatically? Can I change it?](#does-jar2app-figure-the-main-class-of-my-jar-automatically-can-i-change-it)
  * [Apple defines several keys for its App format. How does jar2app figure them out?](#apple-defines-several-keys-for-its-app-format-how-does-jar2app-figure-them-out)
  * [If I only pass the jar and no other options, what are the defaults used by jar2app?](#if-i-only-pass-the-jar-and-no-other-options-what-are-the-defaults-used-by-jar2app)
  * [How is the App name determined?](#how-is-the-app-name-determined)
  * [Where did this idea come from?](#where-did-this-idea-come-from)
  * [Is there a GUI?](#is-there-a-gui)
  * [Does it work on retina screens?](#does-it-work-on-retina-screens)
  * [Should I use jar2app for my commercial application?](#should-i-use-jar2app-for-my-commercial-application)
  * [jar2app doesn't do what I want. Are there other alternatives?](#jar2app-doesnt-do-what-i-want-are-there-other-alternatives)
  * [Example Usage](#example-usage)
    * [Easiest way to bundle](#easiest-way-to-bundle)
    * [Changing App file output name](#changing-app-file-output-name)
    * [Bundle with an icon](#bundle-with-an-icon)
    * [Changing the name that appears in menu bars (Bundle Display Name)](#changing-the-name-that-appears-in-menu-bars-bundle-display-name)
    * [Bundling your own JDK/JRE](#bundling-your-own-jdkjre)
  * [What are all the options?](#what-are-all-the-options)

(TOC created with the help of [gh-md-toc](https://github.com/ekalinin/github-markdown-toc))
    
# Aren't there other tools that do this? Why another one?
There are other tools that do this. I acklowedge them and even have [several links to them](#jar2app-doesnt-do-what-i-want-are-there-other-alternatives).

However, this project was born out of the need to do something easily and without much cruft. Most solutions out there require a gazillion arguments, or installing *ant* and memorizing lots of conventions. **jar2app**, however, tries to keep the power of those utilities while providing high simplicity in the process. Really, isn't it wonderful to have such an easy-to-use interface?

If you're also considering why these contributions  weren't just sent to one of the other projects, it is because this could not be done easily. [Packr](https://github.com/libgdx/packr) uses a custom launcher and is meant to pack things for Mac OS X, Windows and Linux. Most of the other alternatives require third-party tools that embbed other functionality and which simply cannot be stripped. The solution I was left with was just rolling out my own. If you think that's just a strong case of NIH, feel free to grab what you want from me and send a patch to the other projects :) Just follow the GPL!

# Can I submit bundles created with jar2app to the Appstore?
**jar2app** may bundle your jar, but there are several steps you further need to take to submit your application to the Appstore. This is not a limitation of **jar2app**, it's just how the Appstore requires you to do things. For more information on how to submit bundles to the appstore, see [here](http://speling.shemnon.com/blog/2014/04/10/getting-your-java-app-in-the-mac-app-store/) and [here](https://www.jemchicomac.com/how-to-convert-a-jar-file-into-an-app-for-osx/).

# How do I install/uninstall it?
 Just clone the repository and run ``install.sh``, or ``uninstall.sh`` to remove it. It will install to /usr/bin, but you can change this by passing your desired prefix to install.sh, as an argument. This will install the **jar2app** application/script and make it available for you to run.

## Examples:
### Install
    git clone https://github.com/Jorl17/jar2app
    cd jar2app
    chmod +x install.sh uninstall.sh
    sudo ./install.sh
### Install to /usr/local/bin prefix
    git clone https://github.com/Jorl17/jar2app
    cd jar2app
    chmod +x install.sh uninstall.sh
    sudo ./install.sh /usr/local/bin
### Uninstall 
    ./uninstall.sh
### Uninstall from /usr/local/bin prefix
    ./uninstall.sh /usr/local/bin

# How does it work?
**jar2app** relies on [JavaAppLauncher](https://java.net/projects/appbundler) (although you don't need to install anything). This application, officially provided by Oracle (previously Apple), acts as wrapper that starts a JVM with a set of options. The JVM can be bundled with the App file, or the system-wide-one can be used. Essentially, all that **jar2app** has to do is create a directory structure (app files are just directories), pack *JavaAppLauncher* and your application in it and set appropriate values in an *Info.plist* file. Additionally, if you so wish, your own JDK or JRE can be bundled and the *Info.plist* file will be updated to reflect this.

I know that there are other solutions that write their own wrapper, but the provided wrapper seems to work great (it's also  bundled by [Weka](http://www.cs.waikato.ac.nz/ml/weka/)). The other wrapper I saw out there was from the [Packr](https://github.com/libgdx/packr) project and it really depended on their way of doing this.

# What exactly can I change?
You can change many things, but more specifically, you can change the icon, the display name (the one that appears on the menu bar), the version and copyright information, the bundled JDK/JRE and the JVM options. For a full list of options, see [here](#what-are-all-the-options)

# Does jar2app bundle its own JRE/JDK? Can I bundle my own?
By default, **jar2app** doesn't bundle any JRE or JDK, and the default will be used on each system. You can, however, pass it a JRE/JDK with the `-r`,`--runtime` option. It can be supplied as a folder or as a zipfile. This JRE/JDK should match the directory structure found in Oracle's JDK (i.e. the first folder should be named Contents, etc).

# Does jar2app figure the main class of my jar automatically? Can I change it?
Yes it does. It looks inside your jar file for the MANIFEST.MF file and extracts the name of the main class. You can change this behavior, and pass in another main class with the `-m`, `--main-class` option.

# Apple defines several keys for its App format. How does jar2app figure them out?
There are several keys that Apple defines, and you might want to [check them out](https://developer.apple.com/library/ios/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html). **jar2app** assigns values to the following keys:
* **CFBundleDevelopmentRegion**: This is fixed at English
* **CFBundleExecutable**: This is internally defined to *JavaAppLauncher* (from [oracle](https://java.net/projects/appbundler))
* **CFBundleIconFile**: This is set to whichever icon you passed in, and ignored if no icon is used
* **CFBundleIdentifier**: This is chosen from the following, in order:
	1. What you supplied (`-b`,`--bundle-identifier`)
	2. The default: *com.jar2app.example.`application name`*
* **CFBundleDisplayName**: This is chosen from the following, in order:
	1. What you supplied as display name (`-d`,`--display-name`)
	2. What you supplied as bundle name (`-n`,`--name`)
	3. The name of the app (passed as outputfile argument)
	4. The name of the jar (excluding extension)
* **CFBundleName**: This is chosen from the following, in order:
	1. What you supplied as bundle name (`-n`,`--name`)
	2. What you supplied as display name (`-d`,`--display-name`)
	3. The name of the app (passed as outputfile argument)
	4. The name of the jar (excluding extension)
* **CFBundleVersion**: This is chosen from the following, in order:
	1. What you supplied as version (`-v`,`--version`)
	2. What you supplied as short version (`-s`,`--short-version`)
	3. The default: 1.0.0
* **CFBundleShortVersionString**: This is chosen from the following, in order:
	1. What you supplied as short version (`-s`,`--short-version`)
	2. What you supplied as version (`-v`,`--version`)
	3. The default: 1.0.0
* **CFBundleSignature**: This is chosen from what you supply or the string "????".
* **NSHumanReadableCopyright**: This is set to what you supply or the empty string

The `info.plist` file whill contain additional keys, but there are used to pass information to *JavaAppLauncher* (JVM arguments, JDK/JRE, etc)

# If I only pass the jar and no other options, what are the defaults used by jar2app?
**jar2app** assumes that you want to create an app file with **the same basename as your jar file** and in your **current working directory**. It assumes no JRE/JDK is to be bundled, and that no special arguments have to be passed to the JVM. The remaining options, such as the Icon, display name and others, are figured out as [described in here](#apple-defines-several-keys-for-its-app-format-how-does-jar2app-figure-them-out). **The short version is that all names get set to the basename of your jar, and that versions are set to 1.0.0**.

# How is the App name determined?
You are probably also interested in [this question](#if-i-only-pass-the-jar-and-no-other-options-what-are-the-defaults-used-by-jar2app) and [this question](#apple-defines-several-keys-for-its-app-format-how-does-jar2app-figure-them-out). The app name is determined as so:

1. What you supplied as app name (it is the last unnamed argument, e.g. `jar2app in.jar outname`). You don't need to append `.App`, as **jar2app** does it for you.
2. What you supplied as bundle name (`-n`,`--name`)
3. What you supplied as display name (`-d`,`--display-name`)
5. The name of the jar (excluding extension)


# Where did this idea come from?
Well, you should probably check [this FAQ entry first](#arent-there-other-tools-that-do-this-why-another-one). I originally went looking for an application like **jar2app** because I noticed that spotlight didn't like showing me .jar files. This meant that whenever I wanted to launch applications bundled as jars (and that happens *very* often), I'd have to break my workflow and wait while spotlight figured itself out. To fix this, I decided to just package the jar in an app. "It must be easy, right"? Turns out it wasn't so easy and most tools weren't straightforward, so, here's **jar2app**. Have fun, report bugs and add features as you wish!

# Is there a GUI?
This tool is so simple to use that it seems pointless to add a GUI. Nevertheless, for all your command line aversion needs, I might implement a really simple optional GUI in the future (probably using PyQt).

# Does it work on retina screens?
Yes it does. It adds specific entries in the Info.plist file to ensure that retina screen is enabled by default. You can change that by passing `-l`,`--low-res-mode`.

# Should I use jar2app for my commercial application?
You can, but don't expect a one-liner to do the trick. There are several parameters that you have to configure, including special unique keys and signatures. **jar2app** has many defaults that **should not be used** if you intend to distribute your application in very serious fashion. Use it with the default values for simple, easy and straightforward redistribution.

# jar2app doesn't do what I want. Are there other alternatives?
**jar2app** tries to do most of what the other tools do. It's lacking mostly in JRE/JDK minimizing support, and it hasn't really been thoroughly tested when bundling things for the app store.

If it's not your cup of tea, don't worry! There are other alternatives, such as the wonderful [Packr](https://github.com/libgdx/packr), the [official Oracle documentation](http://docs.oracle.com/javase/7/docs/technotes/guides/jweb/packagingAppsForMac.html),  the [official Apple documentation](https://developer.apple.com/library/mac/documentation/Java/Conceptual/Java14Development/03-JavaDeployment/JavaDeployment.html) and the [AppBundler project](https://java.net/projects/appbundler), part of which is used in **jar2app**. You can also read more about the cumbersome nature of packaging jars in app files [here](http://dclunie.blogspot.pt/2014/10/keeping-up-with-mac-java-bundling-into.html).

Even if **jar2app** didn't help, come back and open an issue, or send your own patches!

# Example Usage
Here are a couple of examples on how to change the settings of **jar2app**. For a full list of options, see [here](#what-are-all-the-options).

## Easiest way to bundle
	
    jar2app test.jar

You should now have a `test.App` in your directory.

## Changing App file output name

This can be done in several ways. The most straightforward one is just:

    jar2app test.jar out
    
You should now have a `out.App` in your directory. Note how **jar2app** automatically appends the `.App` extension (this can be disabled with `-a`,`--no-append-app-to-name`). You can also do

    jar2app test.jar out.App
    
Lastly, You can also do

    jar2app test.jar test/out.App
    
And **jar2app** will create the test subdirectory for you. It only creates the parent directory of the target .app file, though!

Also note that the app output name is pre-determined based on other options. For instance, if you pass in a bundle name, that will be used. See [this question](#apple-defines-several-keys-for-its-app-format-how-does-jar2app-figure-them-out) for more details.

## Bundle with an icon
	
    jar2app test.jar -i icon.icns

You should now have a `test.App` in your directory with the provided icon. `-i` can be a full path, e.g.
	
    jar2app test.jar -i /awesomeicons/icon.icns

## Changing the name that appears in menu bars (Bundle Display Name)
The name that appears in menu bars will be given by the *Bundle Display Name*. You can se this with `-d`,`--display-name`, but I'd really recommend that you change the bundle name itself with `-n`,`--name` (the *Bundle Display Name* will assume this value). This can be done with
	
    jar2app test.jar -n "Amazing Application"
    
Note that since in the above example, no output .App name is given, **the .App file will also be named "Amazing Application"** (see [here](#how-is-the-app-name-determined)). You can change this by doing any of:
	
    jar2app test.jar out -n "Amazing Application"
    jar2app test.jar out.app -n "Amazing Application"
    jar2app test.jar -n "Amazing Application" out
    jar2app test.jar -n "Amazing Application" out.app
    
Any of those commands will have the same effect: the app file will be `out.app`, but the display name (shown in menus) will be "Amazing Application".

## Bundling your own JDK/JRE
Say you want to bundle your own JDK/JRE. For instance, assume you want to bundle the one located at `/Library/Java/JavaVirtualMachines/jdk1.8.0_40.jdk`. This is trivial to do (`-r`, `--runtime`), just run:

	jar2app test.jar -r /Library/Java/JavaVirtualMachines/jdk1.8.0_40.jdk

You can also pass the JDK/JRE as a **zip file**. Assume you have it in compressed form in `/compressedJDKs/jdk1.8.0_40.jdk.zip`, just do:

	jar2app test.jar -r /compressedJDKs/jdk1.8.0_40.jdk.zip   
   
# What are all the options?

```
  -h, --help            show this help message and exit
  -n BUNDLE_NAME, --name=BUNDLE_NAME
                        Package/Bundle name.
  -d BUNDLE_DISPLAYNAME, --display-name=BUNDLE_DISPLAYNAME
                        Package/Bundle display name.
  -i ICON, --icon=ICON  Icon (in .icns format). (Default: None)
  -b BUNDLE_IDENTIFIER, --bundle-identifier=BUNDLE_IDENTIFIER
                        Package/Bundle identifier (e.g. com.example.test)
                        (Default is application name prefix by
                        com.jar2app.example..
  -v BUNDLE_VERSION, --version=BUNDLE_VERSION
                        Package/Bundle version (e.g. 1.0.0) (Default: 1.0.0).
  -s SHORT_VERSION_STRING, --short-version=SHORT_VERSION_STRING
                        Package/Bundle short version (see Apple's
                        documentation on CFBundleShortVersionString) (Default:
                        1.0.0).
  -c COPYRIGHT_STR, --copyright=COPYRIGHT_STR
                        Package/Bundle copyright string (e.g. (c) 2015 Awesome
                        Person) (Default: empty)
  -u SIGNATURE, --unique-signature=SIGNATURE
                        4 Byte unique signature of your application (Default:
                        ????)
  -m MAIN_CLASS_NAME, --main-class=MAIN_CLASS_NAME
                        Jar main class. Blank for auto-detection (usually
                        right).
  -r JDK, --runtime=JDK
                        JRE/JDK runtime to bundle. Can be a folder or a zip
                        file. If none is given, the default on the system is
                        used (default: None)
  -j JVM_OPTIONS, --jvm-options=JVM_OPTIONS
                        JVM options. Place one by one, separated by spaces,
                        inside inverted commas (e.g. -o "-Xmx1024M -Xms256M)
                        (Default: None)
  -a, --no-append-app-to-name
                        Do not try to append .app to the output file by
                        default.
  -l, --low-res-mode    Do not try to report retina-screen capabilities (use
                        low resolution mode; by default high resolution mode
                        is used).
```


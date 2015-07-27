from optparse import OptionParser
import os.path
import shutil
import tempfile
from zipfile import ZipFile
from os import rmdir
import sys

__author__ = 'jorl17'

DEFAULT_VERSION='1.0.0'
DEFAULT_BUNDLE_IDENTIFIER_PREFIX='com.jar2app.example.'
DEFAULT_SIGNATURE='????'

info_plist = """<?xml version="1.0" ?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>English</string>

    <key>CFBundleExecutable</key>
    <string>JavaAppLauncher</string>

    <key>CFBundleIconFile</key>
    <string>{icon}</string>

    <key>CFBundleIdentifier</key>
    <string>{bundle_identifier}</string>

    <key>CFBundleDisplayName</key>
    <string>{bundle_displayname}</string>

    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>

    <key>CFBundleName</key>
    <string>{bundle_name}</string>

    <key>CFBundlePackageType</key>
    <string>APPL</string>

    <key>CFBundleShortVersionString</key>
    <string>{short_version_string}</string>

    <key>CFBundleSignature</key>
    <string>{unique_signature}</string>

    <key>CFBundleVersion</key>
    <string>{bundle_version}</string>

    <key>NSHumanReadableCopyright</key>
    <string>{copyright}</string>

    {jdk}

    <key>JVMMainClassName</key>
    <string>{main_class_name}</string>

    <key>JVMOptions</key>
    <array>
{jvm_options}
    </array>

    <key>JVMArguments</key>
    <array>
{jvm_arguments}
    </array>
    </dict>
</plist>
"""

def mkdir_ignore_exists(p):
    try:
        os.mkdir(p)
        return True
    except FileExistsError:
        return False

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(path, mode)

def find_jar_mainclass(jar_file):
    f = ZipFile(jar_file, 'r')
    for file in f.infolist():
        orig_fn = file.filename
        lower_fn = orig_fn.lower()
        if lower_fn.startswith('meta-inf') and lower_fn.endswith('manifest.mf'):
            manifest_mf = f.read(orig_fn)
            for line in manifest_mf.decode().split('\n'):
                if line.strip().lower().startswith('main-class'):
                    return line.split(':')[1].strip()


def build_directory_structure(app_full_path):
    mkdir_ignore_exists(os.path.dirname(app_full_path)) #Base output directory where the app is placed. Create it.
    mkdir_ignore_exists(app_full_path)
    mkdir_ignore_exists(os.path.join(app_full_path, 'Contents'))
    mkdir_ignore_exists(os.path.join(app_full_path, 'Contents', 'Java'))
    mkdir_ignore_exists(os.path.join(app_full_path, 'Contents', 'MacOS'))
    mkdir_ignore_exists(os.path.join(app_full_path, 'Contents', 'PlugIns'))
    mkdir_ignore_exists(os.path.join(app_full_path, 'Contents', 'Resources'))
    mkdir_ignore_exists(os.path.join(app_full_path, 'Contents', 'Resources', 'en.lproj'))

def create_plist_file(destination_folder, icon, bundle_identifier, bundle_displayname, bundle_name,bundle_version,short_version_string,copyright_str, main_class_name, jvm_arguments, jvm_options, jdk, unique_signature):
    filled_info_plist=info_plist.format(icon=icon,
                                        bundle_identifier=bundle_identifier,
                                        bundle_displayname=bundle_displayname,
                                        bundle_name=bundle_name,
                                        bundle_version=bundle_version,
                                        short_version_string=short_version_string,
                                        copyright=copyright_str,
                                        main_class_name=main_class_name,
                                        jvm_arguments=jvm_arguments,
                                        jvm_options=jvm_options,
                                        jdk=jdk,
                                        unique_signature=unique_signature)

    with open(os.path.join(destination_folder, 'Info.plist'), 'w') as f:
        f.write(filled_info_plist)

def copy_jdk(app_full_path, jdk, jdk_isfile):
    if jdk:
        if jdk_isfile:
            tmpdir = tempfile.mkdtemp()
            f = ZipFile(jdk, 'r')
            f.extractall(tmpdir)
            jdk_dir = tmpdir
            try:
                destination_path = os.path.join(app_full_path, 'Contents', 'PlugIns')
                os.rmdir(destination_path)
                shutil.copytree(jdk_dir, destination_path)
            except FileExistsError as e:
                raise # FIXME
            try:
                base_path = os.path.join(app_full_path, 'Contents', 'PlugIns')
                dir = os.listdir(base_path)[0]
                os.rename(os.path.join(base_path, dir),
                          os.path.join(base_path, strip_extension_from_name(os.path.basename(jdk))))
                shutil.rmtree(tmpdir)
            except:
                raise #FIXME
        else:
            shutil.copytree(jdk, os.path.join(app_full_path, 'Contents', 'PlugIns', os.path.basename(jdk)))


def copy_base_files(app_full_path, jar_file, jdk, jdk_isfile):
    #shutil.copyfile(join('basefiles', 'Pkginfo'), join(app_full_path, 'Contents', 'Pkginfo'))
    shutil.copy2(os.path.join('basefiles', 'Localizable.strings'), os.path.join(app_full_path, 'Contents', 'Resources', 'en.lproj', 'Localizable.strings'))
    shutil.copy2(os.path.join('basefiles', 'JavaAppLauncher'), os.path.join(app_full_path, 'Contents', 'MacOS', 'JavaAppLauncher'))
    make_executable(os.path.join(app_full_path, 'Contents', 'MacOS', 'JavaAppLauncher'))
    shutil.copy2(jar_file, os.path.join(app_full_path, 'Contents', 'Java', os.path.basename(jar_file)))

    copy_jdk(app_full_path, jdk, jdk_isfile)


def strip_extension_from_name(name):
    return os.path.splitext(name)[0]

def determine_app_name(jar_name, output, bundle_displayname, bundle_name, auto_append_app):
    if output:
        dir,name = os.path.split(output)
        if not dir:
            dir = '.'
    else:
        dir = '.'
        name = ''

    if not name:
        # If no .app name is provided, prefer:
        # 1. The bundle name, if it was provided
        # 2. the bundle_displayname, if it was provided
        # 3. The jar name
        if bundle_name:
            return os.path.join(dir,bundle_name + '.app')
        elif bundle_displayname:
            return os.path.join(dir,bundle_displayname + '.app')
        elif jar_name:
            return os.path.join(dir,strip_extension_from_name(jar_name) + '.app')
    else:
        # Ensure the name ends with .app, unless we were told not to do so
        if auto_append_app:
            if name.lower().endswith('.app'):
                return os.path.join(dir,name)
            else:
                return os.path.join(dir,name + '.app')
        else:
            return dir,name


def determine_jdk(jdk):
    if not jdk:
        return '',True
    isfile = os.path.isfile(jdk)
    if isfile:
        if not jdk.lower().endswith('.zip'):
            exit('JDK file is not a zip file.')
        jdk = strip_extension_from_name(os.path.basename(jdk))

    return '<key>JVMRuntime</key>\n<string>' + jdk + '</string>',isfile




def string_to_plist_xmlarray_values(s):
    if not s:
        return ''
    return  '        <string>' + '</string>\n        <string>'.join( [i.strip() for i in s.split() ] ) + '</string>'


def make_app(jar_file, output='.', icon=None, bundle_identifier=None, bundle_displayname=None, bundle_name=None, bundle_version=None, short_version_string=None, copyright_str=None, main_class_name=None, jvm_arguments=None, jvm_options=None, jdk=None, unique_signature=None, auto_append_app=True):
    def default_value(d, default):
        return d if d else default

    jar_name = os.path.basename(jar_file)
    app_name_w_extension = determine_app_name(jar_name, output, bundle_displayname, bundle_name, auto_append_app)
    app_name = strip_extension_from_name(os.path.basename(app_name_w_extension))
    icon = default_value(icon, '')
    bundle_identifier = default_value(bundle_identifier, DEFAULT_BUNDLE_IDENTIFIER_PREFIX + app_name)

    if not bundle_displayname:
        # If no bundle_displayname is provided:
        # 1. Use the bundle_name
        # 2. use the app_name (note that the app_name was already determined based on what the user gave us.
        #    For instance, if no app_name was given, and no displayname was given, and no app name was given, the
        #    first choice is the bundle_name.
        if bundle_name:
            bundle_displayname = bundle_name
        else:
            bundle_displayname = app_name

    # When we get here, we always have a displayname. So if there's no bundlename, go with that. It may itself have
    # come from the app name
    bundle_name = default_value(bundle_name, bundle_displayname)

    if not bundle_version:
            bundle_version = short_version_string if short_version_string else DEFAULT_VERSION

    # When we get here, we always have bundle_version, even if it is the default
    short_version_string = default_value(short_version_string, bundle_version)
    copyright_str = default_value(copyright_str, '')
    main_class_name = default_value(main_class_name, find_jar_mainclass(jar_file))
    unique_signature = default_value(unique_signature, '????')
    jvm_arguments = string_to_plist_xmlarray_values(jvm_arguments)
    jvm_options  = string_to_plist_xmlarray_values(jvm_options)
    jdk_xml,jdk_isfile = determine_jdk(jdk)

    build_directory_structure(app_name_w_extension)
    create_plist_file(os.path.join(app_name_w_extension, 'Contents'), icon, bundle_identifier, bundle_displayname, bundle_name,bundle_version,short_version_string,copyright_str, main_class_name, jvm_arguments, jvm_options, jdk_xml, unique_signature)
    copy_base_files(app_name_w_extension, jar_file, jdk, jdk_isfile)

jar_file = '/Users/jorl17/Applications/mcpatcher-5.0.2.jar'

def parse_input():
    parser = OptionParser()
    parser.add_option('-n', '--name', help='Package/Bundle name.', dest='bundle_name', type='string', default=None)
    parser.add_option('-d', '--display-name', help='Package/Bundle display name.', dest='bundle_displayname', type='string',default=None)
    parser.add_option('-i', '--icon',help='Icon (in .icns format). (Default: None)', dest='icon', type='string', default=None)
    parser.add_option('-b', '--bundle-identifier', help='Package/Bundle identifier (e.g. com.example.test) (Default is application name prefix by {}.'.format(DEFAULT_BUNDLE_IDENTIFIER_PREFIX), dest='bundle_identifier',type='string', default=None)
    parser.add_option('-v', '--version', help='Package/Bundle version (e.g. 1.0.0) (Default: {}).'.format(DEFAULT_VERSION),dest='bundle_version', type='string', default=DEFAULT_VERSION)
    parser.add_option('-s', '--short-version', help='Package/Bundle short version (see Apple\'s documentation on CFBundleShortVersionString) (Default: {}).'.format(DEFAULT_VERSION), dest='short_version_string',type='string', default=DEFAULT_VERSION)
    parser.add_option('-c', '--copyright',help='Package/Bundle copyright string (e.g. (c) 2015 Awesome Person) (Default: empty)',dest='copyright_str', type='string', default=None)
    parser.add_option('-u', '--unique-signature', help='4 Byte unique signature of your application (Default: {})'.format(DEFAULT_SIGNATURE),dest='signature', type='string', default=DEFAULT_SIGNATURE)
    parser.add_option('-m', '--main-class', help='Jar main class. Blank for auto-detection (usually right).',dest='main_class_name', type='string', default=None)
    parser.add_option('-r', '--runtime', help='JRE/JDK runtime to bundle. Can be a folder or a zip file. If none is given, the default on the system is used (default: None)',dest='jdk', type='string', default=None)
    parser.add_option('-j', '--jvm-options',help='JVM options. Place one by one, separated by spaces, inside inverted commas (e.g. -o "-Xmx1024M -Xms256M) (Default: None)',dest='jvm_options', type='string', default=None)
    parser.add_option('-a', '--no-append-app-to-name', help='Do not try to append .app to the output file by default.', dest='auto_append_name', action='store_false')

    (options, args) = parser.parse_args()

    if len(args) == 2:
        input_file = args[0]
        output = args[1]
    elif len(args) > 2:
        parser.error('Extra arguments provided!')
    elif len(args) == 1:
        input_file = args[0]
        output = None
    else:
        parser.error('An input file is needed. Optionally, you can also provide an output file or directory. E.g.\n{} in.jar\n{} in.jar out.app\n{} in.jar out/'.format(sys.argv[0], sys.argv[0], sys.argv[0]) )

    if options.auto_append_name == None:
        options.auto_append_name = True

    jvm_arguments = ''
    return input_file, output, options.icon, options.bundle_identifier, options.bundle_displayname, options.bundle_name, options.bundle_version, options.short_version_string, options.copyright_str, options.main_class_name, jvm_arguments, options.jvm_options, options.jdk, options.signature, options.auto_append_name

make_app(*parse_input())

#make_app(jar_file, 'Test/', jdk='jdk1.8.0_40.jdk')
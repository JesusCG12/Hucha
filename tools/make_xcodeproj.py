"""Genera ios/Hucha.xcodeproj/project.pbxproj con los .swift de ios/Hucha, Assets.xcassets y la carpeta Web.

Uso: python3 tools/make_xcodeproj.py ios
"""
import hashlib
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])            # .../ios/Hucha
src = root / "Hucha"
swift_files = sorted(p.name for p in src.glob("*.swift"))
assert swift_files, "no hay archivos Swift"


def oid(name: str) -> str:
    return hashlib.md5(("hucha:" + name).encode()).hexdigest()[:24].upper()


PROJECT, TARGET = oid("project"), oid("target")
MAIN_GROUP, SRC_GROUP, PRODUCTS = oid("group:main"), oid("group:src"), oid("group:products")
PRODUCT = oid("product")
ASSETS_REF, ASSETS_BUILD = oid("ref:assets"), oid("build:assets")
WEB_REF, WEB_BUILD = oid("ref:web"), oid("build:web")
PH_SOURCES, PH_FRAMEWORKS, PH_RESOURCES = oid("phase:sources"), oid("phase:frameworks"), oid("phase:resources")
CL_PROJECT, CL_TARGET = oid("cl:project"), oid("cl:target")
CFG_P_DEBUG, CFG_P_RELEASE = oid("cfg:p:debug"), oid("cfg:p:release")
CFG_T_DEBUG, CFG_T_RELEASE = oid("cfg:t:debug"), oid("cfg:t:release")
ref = {f: oid("ref:" + f) for f in swift_files}
bld = {f: oid("build:" + f) for f in swift_files}

T = "\t"
out = []
w = out.append

w("// !$*UTF8*$!")
w("{")
w(T + "archiveVersion = 1;")
w(T + "classes = {")
w(T + "};")
w(T + "objectVersion = 56;")
w(T + "objects = {")
w("")
w("/* Begin PBXBuildFile section */")
w(f"{T*2}{ASSETS_BUILD} /* Assets.xcassets in Resources */ = {{isa = PBXBuildFile; fileRef = {ASSETS_REF} /* Assets.xcassets */; }};")
w(f"{T*2}{WEB_BUILD} /* Web in Resources */ = {{isa = PBXBuildFile; fileRef = {WEB_REF} /* Web */; }};")
for f in swift_files:
    w(f"{T*2}{bld[f]} /* {f} in Sources */ = {{isa = PBXBuildFile; fileRef = {ref[f]} /* {f} */; }};")
w("/* End PBXBuildFile section */")
w("")
w("/* Begin PBXFileReference section */")
w(f"{T*2}{PRODUCT} /* Hucha.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = Hucha.app; sourceTree = BUILT_PRODUCTS_DIR; }};")
w(f"{T*2}{ASSETS_REF} /* Assets.xcassets */ = {{isa = PBXFileReference; lastKnownFileType = folder.assetcatalog; path = Assets.xcassets; sourceTree = \"<group>\"; }};")
w(f"{T*2}{WEB_REF} /* Web */ = {{isa = PBXFileReference; lastKnownFileType = folder; path = Web; sourceTree = \"<group>\"; }};")
for f in swift_files:
    w(f"{T*2}{ref[f]} /* {f} */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = {f}; sourceTree = \"<group>\"; }};")
w("/* End PBXFileReference section */")
w("")
w("/* Begin PBXFrameworksBuildPhase section */")
w(f"{T*2}{PH_FRAMEWORKS} /* Frameworks */ = {{")
w(f"{T*3}isa = PBXFrameworksBuildPhase;")
w(f"{T*3}buildActionMask = 2147483647;")
w(f"{T*3}files = (")
w(f"{T*3});")
w(f"{T*3}runOnlyForDeploymentPostprocessing = 0;")
w(f"{T*2}}};")
w("/* End PBXFrameworksBuildPhase section */")
w("")
w("/* Begin PBXGroup section */")
w(f"{T*2}{MAIN_GROUP} = {{")
w(f"{T*3}isa = PBXGroup;")
w(f"{T*3}children = (")
w(f"{T*4}{SRC_GROUP} /* Hucha */,")
w(f"{T*4}{PRODUCTS} /* Products */,")
w(f"{T*3});")
w(f"{T*3}sourceTree = \"<group>\";")
w(f"{T*2}}};")
w(f"{T*2}{PRODUCTS} /* Products */ = {{")
w(f"{T*3}isa = PBXGroup;")
w(f"{T*3}children = (")
w(f"{T*4}{PRODUCT} /* Hucha.app */,")
w(f"{T*3});")
w(f"{T*3}name = Products;")
w(f"{T*3}sourceTree = \"<group>\";")
w(f"{T*2}}};")
w(f"{T*2}{SRC_GROUP} /* Hucha */ = {{")
w(f"{T*3}isa = PBXGroup;")
w(f"{T*3}children = (")
for f in swift_files:
    w(f"{T*4}{ref[f]} /* {f} */,")
w(f"{T*4}{ASSETS_REF} /* Assets.xcassets */,")
w(f"{T*4}{WEB_REF} /* Web */,")
w(f"{T*3});")
w(f"{T*3}path = Hucha;")
w(f"{T*3}sourceTree = \"<group>\";")
w(f"{T*2}}};")
w("/* End PBXGroup section */")
w("")
w("/* Begin PBXNativeTarget section */")
w(f"{T*2}{TARGET} /* Hucha */ = {{")
w(f"{T*3}isa = PBXNativeTarget;")
w(f"{T*3}buildConfigurationList = {CL_TARGET} /* Build configuration list for PBXNativeTarget \"Hucha\" */;")
w(f"{T*3}buildPhases = (")
w(f"{T*4}{PH_SOURCES} /* Sources */,")
w(f"{T*4}{PH_FRAMEWORKS} /* Frameworks */,")
w(f"{T*4}{PH_RESOURCES} /* Resources */,")
w(f"{T*3});")
w(f"{T*3}buildRules = (")
w(f"{T*3});")
w(f"{T*3}dependencies = (")
w(f"{T*3});")
w(f"{T*3}name = Hucha;")
w(f"{T*3}productName = Hucha;")
w(f"{T*3}productReference = {PRODUCT} /* Hucha.app */;")
w(f"{T*3}productType = \"com.apple.product-type.application\";")
w(f"{T*2}}};")
w("/* End PBXNativeTarget section */")
w("")
w("/* Begin PBXProject section */")
w(f"{T*2}{PROJECT} /* Project object */ = {{")
w(f"{T*3}isa = PBXProject;")
w(f"{T*3}attributes = {{")
w(f"{T*4}BuildIndependentTargetsInParallel = 1;")
w(f"{T*4}LastSwiftUpdateCheck = 1500;")
w(f"{T*4}LastUpgradeCheck = 1500;")
w(f"{T*4}TargetAttributes = {{")
w(f"{T*5}{TARGET} = {{")
w(f"{T*6}CreatedOnToolsVersion = 15.0;")
w(f"{T*5}}};")
w(f"{T*4}}};")
w(f"{T*3}}};")
w(f"{T*3}buildConfigurationList = {CL_PROJECT} /* Build configuration list for PBXProject \"Hucha\" */;")
w(f"{T*3}compatibilityVersion = \"Xcode 14.0\";")
w(f"{T*3}developmentRegion = es;")
w(f"{T*3}hasScannedForEncodings = 0;")
w(f"{T*3}knownRegions = (")
w(f"{T*4}es,")
w(f"{T*4}Base,")
w(f"{T*3});")
w(f"{T*3}mainGroup = {MAIN_GROUP};")
w(f"{T*3}productRefGroup = {PRODUCTS} /* Products */;")
w(f"{T*3}projectDirPath = \"\";")
w(f"{T*3}projectRoot = \"\";")
w(f"{T*3}targets = (")
w(f"{T*4}{TARGET} /* Hucha */,")
w(f"{T*3});")
w(f"{T*2}}};")
w("/* End PBXProject section */")
w("")
w("/* Begin PBXResourcesBuildPhase section */")
w(f"{T*2}{PH_RESOURCES} /* Resources */ = {{")
w(f"{T*3}isa = PBXResourcesBuildPhase;")
w(f"{T*3}buildActionMask = 2147483647;")
w(f"{T*3}files = (")
w(f"{T*4}{ASSETS_BUILD} /* Assets.xcassets in Resources */,")
w(f"{T*4}{WEB_BUILD} /* Web in Resources */,")
w(f"{T*3});")
w(f"{T*3}runOnlyForDeploymentPostprocessing = 0;")
w(f"{T*2}}};")
w("/* End PBXResourcesBuildPhase section */")
w("")
w("/* Begin PBXSourcesBuildPhase section */")
w(f"{T*2}{PH_SOURCES} /* Sources */ = {{")
w(f"{T*3}isa = PBXSourcesBuildPhase;")
w(f"{T*3}buildActionMask = 2147483647;")
w(f"{T*3}files = (")
for f in swift_files:
    w(f"{T*4}{bld[f]} /* {f} in Sources */,")
w(f"{T*3});")
w(f"{T*3}runOnlyForDeploymentPostprocessing = 0;")
w(f"{T*2}}};")
w("/* End PBXSourcesBuildPhase section */")
w("")

COMMON = [
    ("ALWAYS_SEARCH_USER_PATHS", "NO"),
    ("ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS", "YES"),
    ("CLANG_ANALYZER_NONNULL", "YES"),
    ("CLANG_CXX_LANGUAGE_STANDARD", '"gnu++20"'),
    ("CLANG_ENABLE_MODULES", "YES"),
    ("CLANG_ENABLE_OBJC_ARC", "YES"),
    ("CLANG_ENABLE_OBJC_WEAK", "YES"),
    ("CLANG_WARN_BOOL_CONVERSION", "YES"),
    ("CLANG_WARN_EMPTY_BODY", "YES"),
    ("CLANG_WARN_INFINITE_RECURSION", "YES"),
    ("CLANG_WARN_UNREACHABLE_CODE", "YES"),
    ("COPY_PHASE_STRIP", "NO"),
    ("ENABLE_STRICT_OBJC_MSGSEND", "YES"),
    ("ENABLE_USER_SCRIPT_SANDBOXING", "YES"),
    ("GCC_C_LANGUAGE_STANDARD", "gnu17"),
    ("GCC_NO_COMMON_BLOCKS", "YES"),
    ("GCC_WARN_ABOUT_RETURN_TYPE", "YES_ERROR"),
    ("GCC_WARN_UNUSED_FUNCTION", "YES"),
    ("GCC_WARN_UNUSED_VARIABLE", "YES"),
    ("IPHONEOS_DEPLOYMENT_TARGET", "16.0"),
    ("MTL_FAST_MATH", "YES"),
    ("SDKROOT", "iphoneos"),
]
DEBUG_ONLY = [
    ("DEBUG_INFORMATION_FORMAT", "dwarf"),
    ("ENABLE_TESTABILITY", "YES"),
    ("GCC_DYNAMIC_NO_PIC", "NO"),
    ("GCC_OPTIMIZATION_LEVEL", "0"),
    ("GCC_PREPROCESSOR_DEFINITIONS", ['"DEBUG=1"', '"$(inherited)"']),
    ("MTL_ENABLE_DEBUG_INFO", "INCLUDE_SOURCE"),
    ("ONLY_ACTIVE_ARCH", "YES"),
    ("SWIFT_ACTIVE_COMPILATION_CONDITIONS", '"DEBUG $(inherited)"'),
    ("SWIFT_OPTIMIZATION_LEVEL", '"-Onone"'),
]
RELEASE_ONLY = [
    ("DEBUG_INFORMATION_FORMAT", '"dwarf-with-dsym"'),
    ("ENABLE_NS_ASSERTIONS", "NO"),
    ("MTL_ENABLE_DEBUG_INFO", "NO"),
    ("SWIFT_COMPILATION_MODE", "wholemodule"),
    ("VALIDATE_PRODUCT", "YES"),
]
TARGET_SETTINGS = [
    ("ASSETCATALOG_COMPILER_APPICON_NAME", "AppIcon"),
    ("ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME", "AccentColor"),
    ("CODE_SIGN_STYLE", "Automatic"),
    ("CURRENT_PROJECT_VERSION", "1"),
    ("DEVELOPMENT_TEAM", '""'),
    ("ENABLE_PREVIEWS", "YES"),
    ("GENERATE_INFOPLIST_FILE", "YES"),
    ("INFOPLIST_KEY_CFBundleDisplayName", "Hucha"),
    ("INFOPLIST_KEY_LSApplicationCategoryType", '"public.app-category.finance"'),
    ("INFOPLIST_KEY_UIApplicationSceneManifest_Generation", "YES"),
    ("INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents", "YES"),
    ("INFOPLIST_KEY_UILaunchScreen_Generation", "YES"),
    ("INFOPLIST_KEY_UISupportedInterfaceOrientations", "UIInterfaceOrientationPortrait"),
    ("INFOPLIST_KEY_ITSAppUsesNonExemptEncryption", "NO"),
    ("LD_RUNPATH_SEARCH_PATHS", ['"$(inherited)"', '"@executable_path/Frameworks"']),
    ("MARKETING_VERSION", "1.0"),
    ("PRODUCT_BUNDLE_IDENTIFIER", "es.jesuscg12.hucha"),
    ("PRODUCT_NAME", '"$(TARGET_NAME)"'),
    ("SWIFT_EMIT_LOC_STRINGS", "YES"),
    ("SWIFT_VERSION", "5.0"),
    ("TARGETED_DEVICE_FAMILY", "1"),
]


def config(cid: str, name: str, settings) -> None:
    w(f"{T*2}{cid} /* {name} */ = {{")
    w(f"{T*3}isa = XCBuildConfiguration;")
    w(f"{T*3}buildSettings = {{")
    for key, value in sorted(settings):
        if isinstance(value, list):
            w(f"{T*4}{key} = (")
            for item in value:
                w(f"{T*5}{item},")
            w(f"{T*4});")
        else:
            w(f"{T*4}{key} = {value};")
    w(f"{T*3}}};")
    w(f"{T*3}name = {name};")
    w(f"{T*2}}};")


w("/* Begin XCBuildConfiguration section */")
config(CFG_P_DEBUG, "Debug", COMMON + DEBUG_ONLY)
config(CFG_P_RELEASE, "Release", COMMON + RELEASE_ONLY)
config(CFG_T_DEBUG, "Debug", TARGET_SETTINGS)
config(CFG_T_RELEASE, "Release", TARGET_SETTINGS)
w("/* End XCBuildConfiguration section */")
w("")
w("/* Begin XCConfigurationList section */")
for cid, label, a, b in ((CL_PROJECT, 'PBXProject "Hucha"', CFG_P_DEBUG, CFG_P_RELEASE), (CL_TARGET, 'PBXNativeTarget "Hucha"', CFG_T_DEBUG, CFG_T_RELEASE)):
    w(f"{T*2}{cid} /* Build configuration list for {label} */ = {{")
    w(f"{T*3}isa = XCConfigurationList;")
    w(f"{T*3}buildConfigurations = (")
    w(f"{T*4}{a} /* Debug */,")
    w(f"{T*4}{b} /* Release */,")
    w(f"{T*3});")
    w(f"{T*3}defaultConfigurationIsVisible = 0;")
    w(f"{T*3}defaultConfigurationName = Release;")
    w(f"{T*2}}};")
w("/* End XCConfigurationList section */")
w(T + "};")
w(f"{T}rootObject = {PROJECT} /* Project object */;")
w("}")

text = "\n".join(out) + "\n"
dest = root / "Hucha.xcodeproj" / "project.pbxproj"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(text, encoding="utf-8")

# ---- comprobaciones ----
body = re.sub(r"/\*.*?\*/", "", text)
defined = set(re.findall(r"^\t\t([0-9A-F]{24})\s+= \{", body, flags=re.M))
used = set(re.findall(r"\b[0-9A-F]{24}\b", body))
assert used == defined, (used - defined, defined - used)
ids = [ref[f] for f in swift_files] + [bld[f] for f in swift_files]
assert len(set(ids)) == len(ids) and len(defined) == len(swift_files) * 2 + 19, len(defined)
print("pbxproj:", len(swift_files), "archivos Swift,", len(defined), "objetos ->", dest)

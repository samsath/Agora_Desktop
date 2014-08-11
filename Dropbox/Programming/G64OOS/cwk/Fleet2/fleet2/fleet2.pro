TEMPLATE = app
CONFIG += console
CONFIG -= app_bundle
CONFIG -= qt
CONFIG += c++11

SOURCES += main.cpp \
    fleet.cpp

HEADERS += \
    fleet.h

OTHER_FILES += \
    sxh33m_fleet.dat


unix {
    libstocopy.files = sxh33m_fleet.dat
}

unix {
    CONFIG(debug, debug|release): OUTDIR = debug
    else: OUTDIR = release
}

libstocopy.path = $$OUT_PWD/$$OUTDIR
INSTALLS += libstocopy

import QtQuick
import QtQuick.Controls

Item {
    id: root
    width: 1024
    height: 600
    visible: true // Ensure root is visible

    // Dimmer
    Rectangle {
        id: shield
        anchors.fill: parent
        color: "black"
        opacity: 0.6
        visible: true

        MouseArea {
            anchors.fill: parent
            onClicked: root.closeRequested()
        }
    }

    // Main Box
    Rectangle {
        id: popoutBox
        width: 420
        height: 320
        // Force it to the center of the 1024x600 screen
        x: 302 
        y: 140
        color: "#121212"
        border.color: "cyan"
        border.width: 3
        visible: true

        PinchArea {
            anchors.fill: parent
            pinch.target: popoutBox
            
            DragHandler { target: popoutBox }

            Text {
                anchors.centerIn: parent
                text: "IF YOU SEE THIS, QML IS WORKING"
                color: "white"
                font.pixelSize: 20
            }
            
            Button {
                anchors.bottom: parent.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.margins: 20
                text: "CLOSE"
                onClicked: root.closeRequested()
            }
        }
    }
    
    signal closeRequested()
}
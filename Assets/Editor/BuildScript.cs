using System.Collections.Generic;

using UnityEditor;

public class BuildScript
{
    private static string ANDROID_BUILD_PATH = "Build/Android/";

    static void SetAndroid(bool release)
    {
        EditorUserBuildSettings.SwitchActiveBuildTarget(BuildTargetGroup.Android, BuildTarget.Android);
        EditorUserBuildSettings.buildAppBundle = release;
    }

    static void BuildAndroid(bool release)
    {
        BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();

        string extension = release == true ? ".aab" : ".apk";
        buildPlayerOptions.locationPathName = ANDROID_BUILD_PATH + "Test" + extension;

        if (release)
            buildPlayerOptions.options = BuildOptions.CompressWithLz4HC;
        else
        {
            buildPlayerOptions.options = BuildOptions.Development;
            buildPlayerOptions.options = BuildOptions.CompressWithLz4;
        }

        buildPlayerOptions.scenes = GetScenes();
        buildPlayerOptions.target = BuildTarget.Android;
        buildPlayerOptions.targetGroup = BuildTargetGroup.Android;

        BuildPipeline.BuildPlayer(buildPlayerOptions);
    }

    [MenuItem("BuildTest/APK")]
    public static void BuildAndroidAPK()
    {
        SetAndroid(release: false);

        BuildAndroid(release: false);
    }

    public static void BuildAndroidAAB()
    {
        SetAndroid(release: true);

        BuildAndroid(release: true);
    }

    private static string[] GetScenes()
    {
        EditorBuildSettingsScene[] scenes = EditorBuildSettings.scenes;

        List<string> sceneList = new List<string>();

        foreach (EditorBuildSettingsScene scene in scenes)
        {
            if (scene.enabled)
                sceneList.Add(scene.path);
        }

        return sceneList.ToArray();
    }
}
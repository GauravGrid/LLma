import {create} from "zustand";
import {persist} from "zustand/middleware";

let appStore = (set) =>({
    dopen:true,
    fileContent: "",
    selectedFileID : null,
    fileName : null,
    isGenButtonClicked : false,

    updateOpen: (dopen) => set((state) =>({dopen:dopen})),
    updateFileContent: (fileContent) => set((state) => ({ fileContent })),
    updateSelectedFileID : (selectedFileID) => set((state)=>({selectedFileID})),
    updateFileName : (fileName) => set((state)=>({fileName})),
    setIsGenButtonClicked : (isGenButtonClicked) => set((state)=>({isGenButtonClicked})),
    resetState: () =>
    set({
      dopen: true,
      fileContent: "",
      selectedFileID: null,
      fileName: null,
      isGenButtonClicked: false,
    }),
});

appStore = persist(appStore,{name : "my_app_store"});
const useAppStore = create(appStore);
export default useAppStore 
















import { Upload, Button, message } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import { questionApi } from "../../entities/question/api/questionApi.js";

export const FileUpload = ({ onUploadSuccess }) => {
  const props = {
    customRequest: async ({ file, onSuccess, onError }) => {
      try {
        await questionApi.uploadFile(file);
        message.success("Файл загружен");
        onSuccess("ok");

        if (onUploadSuccess) onUploadSuccess();

      } catch {
        message.error("Ошибка загрузки");
        onError("err");
      }
    },
  };

  return (
    <Upload {...props} showUploadList={false}>
      <Button icon={<UploadOutlined />}>Загрузить файл</Button>
    </Upload>
  );
};

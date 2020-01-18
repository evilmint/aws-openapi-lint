class AwsOpenapiLint < Formula
  desc "AWS Gateway Integration linter for OpenAPI 3.0.x specs"
  homepage "https://github.com/evilmint/aws-openapi-lint"
  head "https://github.com/evilmint/aws-openapi-lint.git"
  url "https://github.com/evilmint/aws-openapi-lint.git", :using => :git

  depends_on "python"

  resource "PyYAML" do
    url "https://files.pythonhosted.org/packages/e3/e8/b3212641ee2718d556df0f23f78de8303f068fe29cdaa7a91018849582fe/PyYAML-5.1.2.tar.gz"
    sha256 "01adf0b6c6f61bd11af6e10ca52b7d4057dd0be0343eb9283c878cf3af56aee4"
  end

  def install
    venv = virtualenv_create(libexec, "python3")
    venv.pip_install resources
    venv.pip_install_and_link buildpath
  end
end

# frozen_string_literal: true

module SP
  # Sets up a repo review badge
  class RepoReview < Liquid::Tag
    def initialize(tag_name, markup, tokens)
      super
      @code = markup.strip
      raise SyntaxError, 'RepoReview requires a code' unless @code
      raise SyntaxError, 'RepoReview code must not contain a space' if @code.include? ' '
    end

    def render(_context)
      %(<span class="rr-btn" id="#{@code}">#{@code}</span>)
    end
  end
end

Liquid::Template.register_tag('rr', SP::RepoReview)

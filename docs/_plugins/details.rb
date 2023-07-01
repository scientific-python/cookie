# frozen_string_literal: true

module SP
  # Sets up a details / summary block
  class Details < Liquid::Block
    def initialize(tag_name, markup, tokens)
      super
      @title = markup.strip
    end

    def render(context)
      <<~RETURN
        <details markdown="1">
        <summary>#{@title}</summary>
        #{super}
        </details>
      RETURN
    end
  end
end

Liquid::Template.register_tag('details', SP::Details)
